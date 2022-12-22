import re
import xlsxwriter
opDic= {
    ('STRING_LITRAL', r'".*"'),
    ('COMMENT_STARTER',"#"),
    ('LBRACKET', '('),       
    ('RBRACKET', ')'),       
    ('LBRACE', '{'),         
    ('RBRACE', '}'),         
    ('COMMA', ','),            
    ('SEMICOLON', ';'),        
    ('COLON',':'),            
    ('EQ', '=='),             
    ('NE', '!='),             
    ('LE', '<='),             
    ('GE', '>='),             
    ('LT', '<'),              
    ('GT', '>'),              
    ('NOT', 'not'),
    ('OR', 'or'),           
    ('AND', 'and'),             
    ('ASSIGNMENT', '='),
    ('PLUS', '+'),('PLUS', '+='),           
    ('MINUS', '-'),('MINUS', '-='),   
    ('MULT', '*'),('MULT', '*='),           
    ('DIV', '/'),('DIV', '/='),
    ('MOD', '%'),('MOD', '%='),
    ('FLOORDIV', '//'),('FLOORDIV', '//='), 
    ('POw','**'),('POw','**='),
    ('LEFTSHIFT',"<<"),('LEFTSHIFT',"<<="),
    ('RIGHTSHIFT',">>"),('RIGHTSHIFT',">>="),
    ('BitwiseXOR',"^"),('BitwiseXOR',"^="),
    ('BitwiseOR',"|"),('BitwiseOR',"|="),
    ('BitwiseAND',"&"),('BitwiseAND',"&="),
    ('FLOAT_CONST', r'\d(\d)*\.\d(\d)*'),   # FLOAT
    ('INTEGER_CONST', r'\d(\d)*'),          # INT
    ('NEWLINE', r'\n'),         # NEW LINE
    ('SKIP', r'[ \t]+'),        # SPACE and TABS
    ('MISMATCH', r'.'),         
    ('IDENTITY', 'is'), ('IDENTITY', 'is not'),
    ('MemBERSHIP', 'in'), ('MemBERSHIP', 'not in'),
    ('ID', r'^[^0-9]\w*'),
    }

keywordList = ['and', 'as', 'assert', 'break', 'class', 'def', 'del',
           'elif', 'else', 'except', 'exec', 'finally', 'for', 'from', 'global', 'if', 'import',
           'in', 'is', 'lambda', 'not', 'or', 'pass', 'print', 'raise', 'return', 'try', 'while', 'with', 'yield']


def isKeyword(str):
    return str in keywordList


def main():
    
        path = input("Enter path of input scipt file:")
        outpath = input("Enter path of output excel file:")
        
        f = open(path, 'r')
        lines = f.readlines()
        if len(lines) <= 0:
            print("Input file %s is empty" % f)
            quit(0)
        buf=''
        for line in lines:
            buf+=line  
        
        tokens_join = '|'.join('(?P<%s>%s)' % x for x in opDic)

        workbook = xlsxwriter.Workbook(outpath)
        worksheet = workbook.add_worksheet()
        row=0
        commentFLAG = False
        for item in re.finditer(tokens_join, buf):
            tokenType = item.lastgroup
            token = item.group(type)
            
            if ((tokenType == 'NEWLINE') and (commentFLAG==True)):
                commentFLAG = False
            if tokenType== "COMMENTSTARTER":
                commentFLAG = True
            elif(commentFLAG==True):
                worksheet.write(row, 1, token)
                worksheet.write(row, 2, "COMMENT")
                row += 1
                continue;
            elif tokenType == 'SKIP':
                continue;
            elif (tokenType=="ID" and isKeyword(token)):
                worksheet.write(row, 1, token)
                worksheet.write(row, 2, "KEYWORD")
                row += 1    
            else:
                worksheet.write(row, 1, token)
                worksheet.write(row, 2, tokenType)
                row += 1
        print("(ENDMARKER)")




if __name__ == "__main__":
    main()