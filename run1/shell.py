
import PiyuLang

while (True):
    text=input("PiyuLang >")
    
    result,error=PiyuLang.run('<stdin>',text)
    if error:
        print(error.as_string())
    else:
        print(result)