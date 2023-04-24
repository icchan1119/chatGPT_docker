import random, string

class Security:

    #ランダム英数字生成
    def randomname(self,n):
        randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
        return ''.join(randlst)