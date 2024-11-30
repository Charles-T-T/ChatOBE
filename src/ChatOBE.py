import openai
import markdown
import config


class ChatOBE:
    """
    ChatOBE
    """

    def __init__(self, max_history_len=2000):
        # 没把 api_key 配置到环境变量的话，需要把下面这行注释取消
        # self.api_key = config.OPENAI_API_KEY

        self.prompt = config.PROMPT
        self.chat_history = []  # 对话历史

    def chat(self, query, db_results):
        """获取ai的回复

        Args:
            query(str): 用户发送的内容

        Returns:
            ai_message(str): ai根据用户发送内容给出的回复
        """
        user_message = []  # 用户这次发送的信息（整合prompt和聊天记录后的）
        user_message.append({"role": "system", "content": self.prompt})
        self.chat_history.append({"role": "user", "content": query})

        # TODO 这部分仅用于测试chatobe能否顺利读取后端mysql数据，后续要改
        # 如果有数据库查询结果，将其整合到发送信息中
        if db_results:
            db_context = f"数据库查询结果如下：\n {db_results}"
            self.chat_history.append({"role": "system", "content": db_context})

        user_message.extend(self.chat_history)

        # TODO openai的api还提供其他许多参数，可以考虑修改
        response = openai.chat.completions.create(
            model=config.MODEL, messages=user_message
        )

        # TODO 考虑聊天记录长度限制，另写一个方法维护聊天记录
        # 获取 ai 回复并添加到聊天记录中
        ai_message = response.choices[0].message.content.strip()
        ai_message = ai_message = ai_message.replace("| |", "|\n|").replace("\\n", "\n")
        ai_message = markdown.markdown(ai_message)
        self.chat_history.append({"role": "assistant", "content": ai_message})

        return ai_message
