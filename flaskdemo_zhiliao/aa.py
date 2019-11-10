

def my_log(fun):
    def warp():
        print('warp')
        fun()
    return warp

@my_log
def run():
    print('-----run--')
run()