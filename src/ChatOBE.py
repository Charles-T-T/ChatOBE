import openai
import markdown

import config
import utils


class ChatOBE:
    """
    ChatOBE
    """

    def __init__(self, max_tokens=4000):
        # 没把 api_key 配置到环境变量的话，需要把下面这行注释取消
        # self.api_key = config.OPENAI_API_KEY

        self.prompt = config.PROMPT
        self.summary_prompt = config.SUMMARY_PROMPT
        self.max_tokens = max_tokens  # 用户一次最多可发送的token数
        self.chat_history = []  # 聊天记录
        self.chat_summary = []  # 聊天总结
        # self.db_conn = utils.get_db_connection()  # 与数据库的连接

        # 预处理
        self.prompt_tokens = utils.count_token(self.prompt)  # TODO 可能有新的prompt
        self.prompt_tokens += utils.count_token(self.summary_prompt)

    def chat(self, query):
        """获取ai的回复

        Args:
            query(str): 用户发送的内容

        Returns:
           str: ai根据用户发送内容给出的回复
        """
        messages = self.organize_messages(query)

        # # TODO 这部分仅用于测试chatobe能否顺利读取后端mysql数据，后续要改
        # # 如果有数据库查询结果，将其整合到发送信息中
        # if db_results:
        #     db_context = f"数据库查询结果如下：\n {db_results}"
        #     messages.append({"role": "system", "content": db_context})

        # TODO openai的api还提供其他许多参数，可以考虑修改
        response = openai.chat.completions.create(model=config.MODEL, messages=messages)
        ai_message = response.choices[0].message.content.strip()

        # 更新聊天记录
        self.chat_history.append({"role": "user", "content": query})
        self.chat_history.append({"role": "assistant", "content": ai_message})

        return ai_message

    def refresh_history(self, available_tokens):
        """
        刷新聊天记录，以确保发送内容在token数量限制内
        如果超过，则对早期对话进行总结并存储在summaries中

        Args:
            available_tokens (int): 除去prompt和新query后，还可发送的token数
        """
        while True:
            tokens = self.count_history_summary_tokens()
            if tokens <= available_tokens:
                return

            if len(self.chat_history) < 4:
                # 剩余历史记录已经很少，不再总结
                return

            # 提取早期聊天记录进行总结
            summary_messages = self.chat_history[:4]  # 每次总结两轮对话
            remaining_messages = self.chat_history[4:]

            # TODO 考虑把这个也放到config里面
            # 让llm进行总结的prompt
            ask_sum_prompt = (
                "请总结以下对话内容，尽量简洁明了，但是要保留关键信息：\n\n"
            )

            for message in summary_messages:
                role, content = message["role"], message["content"]
                ask_sum_prompt += f"{role}: {content}"

            summary_response = openai.chat.completions.create(
                model=config.MODEL,
                messages=[
                    {"role": "system", "content": self.prompt},
                    {"role": "user", "content": ask_sum_prompt},
                ],
            )
            summary = summary_response.choices[0].message.content.strip()

            self.chat_summary.append(summary)
            self.chat_history = remaining_messages

    def organize_messages(self, query):
        """
        将用户发送的内容与聊天记录、聊天总结、prompt整合
        并整理为符合api接收的格式

        Args:
            query (str): 用户发送的内容

        Returns:
            list: 整合后待发送给chatobe的内容
        """
        messages = [{"role": "system", "content": self.prompt}]

        # 刷新聊天记录，确保最终发送消息的长度在token限制内
        query_tokens = utils.count_token(query)
        available_tokens = self.max_tokens - self.prompt_tokens - query_tokens
        self.refresh_history(available_tokens)

        # 如果有聊天的总结，将其添加到prompt之后
        if self.chat_summary:
            messages.append({"role": "system", "content": self.summary_prompt})
            for summary in self.chat_summary:
                messages.append({"role": "system", "content": summary})

        # 添加聊天记录
        messages.extend(self.chat_history)

        # 添加本次query
        messages.append({"role": "user", "content": query})

        # 如果需要操作数据库，添加sql结果
        if self.sql_needed(messages):
            # NOTE debug
            print("need sql.")
            result = self.get_sql_result(messages)
            if result:
                # NOTE debug
                print("get sql result: ", result)
                messages.append(
                    {"role": "system", "content": config.SQL_RESULT_PROMPT + result}
                )

        return messages

    def count_history_summary_tokens(self):
        """计算当前聊天记录和聊天总结的总token数

        Returns:
            int: chat_history和chat_summary的总token数
        """
        count = 0
        for message in self.chat_history:
            for key, value in message.items():
                count += utils.count_token(key)
                count += utils.count_token(value)
                # TODO 考虑把每条message元数据的token也计入，但这个因模型而异

        for message in self.chat_summary:
            for key, value in message.items():
                count += utils.count_token(key)
                count += utils.count_token(value)

        return count

    def sql_needed(self, messages):
        """判断是否需要操作数据库才能处理用户的新消息

        Args:
            messages: 包含新消息的对话列表

        Returns:
            bool: 是否需要操作数据库
        """
        new_msgs = messages.copy()
        new_msgs.append({"role": "system", "content": config.CHECK_SQL_PROMPT})
        response = openai.chat.completions.create(model=config.MODEL, messages=new_msgs)
        answer = response.choices[0].message.content.strip()
        return "True" in answer

    def get_sql_result(self, messages):
        """获取sql操作的结果"""
        new_msgs = messages.copy()
        new_msgs.append({"role": "system", "content": config.GET_SQL_PROMPT})
        response = openai.chat.completions.create(model=config.MODEL, messages=new_msgs)
        answer = response.choices[0].message.content.strip()
        # NOTE debug
        print("llm's answer: ", answer)
        if utils.sql_in_text(answer):
            sql = utils.extract_sql(answer)
            # NOTE debug
            print("llm's sql: ", sql)
            result = utils.query_database(sql)
            return str(result)
        else:
            return None
