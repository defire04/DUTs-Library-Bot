from controllers import Parser
from database import DatabaseConnect

url = 'https://www.dut.edu.ua/ua/lib/1/category/2122'

if __name__ == '__main__':
    Parser.start(url)
    DatabaseConnect.replace_C()
    DatabaseConnect.finalize()
