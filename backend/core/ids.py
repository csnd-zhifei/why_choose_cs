"""业务主键生成

DDL 里 users.userid / posts.postid / comments.commentid 都是 bigint 且非自增，
由应用侧生成。这里用「毫秒时间戳 + 3 位随机数」，够本地/小规模使用；
如果要上生产建议换雪花算法或号段模式。
"""
import random
import time


def gen_id() -> int:
    return int(time.time() * 1000) * 1000 + random.randint(0, 999)
