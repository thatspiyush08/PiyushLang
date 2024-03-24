TT_INT = 'TT_INT'
TT_FLOAT = 'TT_FLOAT'
TT_PLUS = 'TT_PLUS'
TT_MINUS = 'TT_MINUS'
TT_MUL = 'TT_MUL'
TT_DIV = 'TT_DIV'
TT_LPAREN = 'TT_LPAREN'
TT_RPAREN = 'TT_RPAREN'


class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}:{self.details}'
        # result+=f'File {self.pos.fn},line {self.pos.ln+1}'
        return result


class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, error_name, details):
        super().__init__(pos_start, pos_end, error_name, details)
# class IllegalCharError(Error):
#         def __init__(self,details):
#             super().__init__(self.start,self.pos_end,'Illegal Character',details)


class Position:
    def __init__(self,idx,ln,col,fn,ftxt):
        self.fn=fn
        self.ftxt=ftxt
        self.idx=idx
        self.ln=ln
        self.col=col
    def advance(self,current_char):
        self.idx+=1
        self.col+=1
        if current_char=='\n':
            ln+=1
            col=0
        return self
    
    def copy(self):
        return Position(self.idx,self.ln,self.col,self.fn,self.ftxt)
        
class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value:return f'{self.type}:{self.value}'
        return f'{self.type}'
    
class Lexer:
    def __init__(self,fn,text):
        self.fn=fn
        self.text=text
        self.pos=Position(-1,0,-1,fn,text)
        self.current_char=None
        self.advance()
    
    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char=self.text[self.pos.idx] if self.pos.idx<len(self.text) else None
        
        
    def make_tokens(self):
        tokens = []
        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in '0123456789':
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS, None))  # Pass None as the value
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS, None))  # Pass None as the value
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL, None))  # Pass None as the value
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV, None))  # Pass None as the value
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN, None))  # Pass None as the value
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN, None))  # Pass None as the value
                self.advance()
            else:
                pos_start=self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start,self.pos,"'" + char + "'")
        return tokens, None  # Return tokens and no error
    def make_number(self):
        num_str=''
        dot_count=0
        while self.current_char!=None and self.current_char in '0123456789.':
            if self.current_char=='.':
                if dot_count==1:break
                dot_count+=1
                num_str+=self.current_char
            else:
                num_str+=self.current_char
            self.advance()
        if dot_count==0:
            return Token(TT_INT,int(num_str))
        else:
            return Token(TT_FLOAT,float(num_str))
        
        
def run(fn,text):
    lexer = Lexer(fn,text)
    tokens, error = lexer.make_tokens()
    return tokens, error
