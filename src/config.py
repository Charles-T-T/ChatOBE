# 主页欢迎语
# TODO 最后按照实际功能写
WELCOME_MSG = """
欢迎使用ChatOBE~ \n 
我是结合了大语言模型的OBE系统，可以帮你进行选课、查询等等。
需要我帮你做些什么？
你可以问我：\n
这学期我有哪些课？ \n
离散数学在哪个教室上？
"""


# 数据库配置
# NOTE 下面默认是游客配置，只有相关数据的select权限
DATABASE_CONFIG = {
    "host": "120.46.194.18",
    "user": "vistor",
    "password": "visit_obe12138",
    "port": 3306,
    "charset": "utf8mb4",
    "database": "sc",
}
SQL_START = "<sql>"
SQL_END = "</sql>"

# LLM配置
# author: FHT
# NOTE 这里用的是我自己的openai-api-key
# github保护机制不允许上传
# 所以运行的时候要把下面这行注释取消，并换成群里的key
OPENAI_API_KEY = "your-key"
MODEL = "gpt-4o"

# 各种prompt
PROMPT = """
你是一款课业管理助手（名叫ChatOBE），可以帮助用户管理选课信息、作业、成绩等内容。
你面向的用户可能是学生，也可能是老师，用户不同时你的功能会有一定的差异。
请用专业且友好的语气回答用户的问题。
请注意，用户发送给你的消息中，可能有需要用到数据库才能正确回答的问题。
请牢记这些内容，记住你的功能和任务。
"""

SUMMARY_PROMPT = "下面是先前聊天记录的总结：\n\n"

CHECK_SQL_PROMPT = """请根据上面的对话记录，判断最新的消息是否需要操作数据库才能解决，
是的话回答True，否则回答False：\n\n"""

SQL_RESULT_PROMPT = "下面是数据库操作的结果，如果之后需要展示的话，最好用表格形式：\n\n"

GET_SQL_PROMPT = """用户的消息需要操作数据库才能给出准确的答复，
请生成相应的sql语句，并用 <sql>和</sql>作为开始和结束sql语句的标志，
例如： <sql>SELECT * FROM course;</sql> \n
数据库中表的结构如下：
\n
课程信息：
CREATE TABLE obe.Course (
    CourseID INT AUTO_INCREMENT PRIMARY KEY,
    CourseName VARCHAR(20) NOT NULL,
    Credit SMALLINT NOT NULL,
    Semester TINYINT NOT NULL,
    Information TEXT,
    CHECK (Semester BETWEEN 1 AND 8)
);
\n
上课时间地点信息：
CREATE TABLE obe.CourseSchedule (
    ScheduleID INT PRIMARY KEY,
    CourseID INT NOT NULL,
    WeekDay ENUM('MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'),
    StartTime TIME NOT NULL,
    EndTime TIME NOT NULL,
    Room VARCHAR(20) NOT NULL,
    Building VARCHAR(20) NOT NULL,

    FOREIGN KEY (CourseID) REFERENCES obe.Course(CourseID) ON DELETE CASCADE,
    CHECK (EndTime > StartTime)
);
\n
请注意，你只能针对上面的表进行操作。
"""
