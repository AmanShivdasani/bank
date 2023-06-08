from flask import Flask,render_template,request,session

app =Flask(__name__)
app.config['SECRET_KEY']="AMAN"
@app.route("/bank")
def bank():
    a=render_template("bankapplication.html")
    return a
@app.route("/otp", methods =["POST","GET"])
def otp():
    account =request.form["account"]
    contact =request.form["contact"]
    record=open("record.txt","r")
    data=record.read()
    record.close()
    data= data.split("\n")
    for i in data:
        if account in i[0:4]:
            if contact in i and contact== i.split(" ")[3]:
                session["data"]=i
                a= render_template("otp.html")
                return a
            else:
                return """<center style = "color: red;">Sorry No record found!</center>
                <br>
                <a href="/logout.html>Home</a>"""
    return render_template("forgot.html")
@app.route("/forgot")
def forgot():
    return render_template("forgot.html")
@app.route("/amount_reduce")
def amount_reduce():
    amount= request.args.get("amount")
    data=session.get('data')
    file=open("record.txt","r")
    newdata=data.split(" ")
    newdata[4]=str(int(newdata[4])-int(amount))
    newdata=" ".join(newdata)
    record=file.read()
    file.close()
    record=record.replace(data,newdata,)
    file=open("record.txt","w")
    file.write(record)
    file.close()
    transaction=open("bank_data\\"+data[0:4]+".txt","a")
    transaction.write("-"+amount+"\n")
    transaction.close()
    session["data"]=newdata
    a=render_template("amount.html",amount=amount)
    return a
@app.route("/amount_add")
def amount():
    amount= request.args.get("amount")
    data=session.get('data')
    file=open("record.txt","r")
    newdata=data.split(" ")
    newdata[4]=str(int(newdata[4])+int(amount))
    newdata=" ".join(newdata)
    record=file.read()
    file.close()
    record=record.replace(data,newdata,)
    file=open("record.txt","w")
    file.write(record)
    file.close()
    transaction=open("bank_data\\"+data[0:4]+".txt","a")
    transaction.write(amount+"\n")
    transaction.close()
    session["data"]=newdata
    a=render_template("amount.html",amount=amount)
    return a
@app.route("/logout")
def logout():
    a=render_template("logout.html")
    return a
@app.route("/verify", methods =["GET","PUT"])
def verify():
    f_name = request.args.get("f_name")
    l_name = request.args.get("l_name")
    email = request.args.get("emaill")
    balance = request.args.get("balance")
    contact =request.args.get("contact")
    pass1 = request.args.get("pass1")
    pass2 = request.args.get("pass2")
    if pass1 == pass2 and len(pass1)>=8 and f_name != "" and l_name != "" and contact !="" and email !="":
        #To take the uniques account numbers 
        record_file="token.txt"
        record= open(record_file,"r")
        accountdata=record.read()
        num=(accountdata)
        record.close()
        #To increase the account number so that it will remain unique
        recordnew=open(record_file,"w")
        recordnew.write(str(int(num)+1))
        recordnew.close()
        line=num+" "+f_name+" "+l_name +" "+ contact +" "+ balance+" "+ pass1 +" "+"\n"
        data_record=open("record.txt","a")
        data_record.write(line)
        data_record.close()
        session["data"]=line
        file=open("bank_data\\"+num+".txt","w")
        file.close()
        return f"""
        <style>h1{{background-color:cyan; color:red }}</style>
        <center><h1>Welcome to python bank </h1>
        <font color="rgb" size="60">
        Your account number is {num}.
        Please note it down for further use.
        Store it at a safe place.
        <br>
        <a href="/logout">Home</a>
        </font</center>
        <marquee>This application is for developer purpose only.It should not be used for production servers.</marquee>
        """
    else:
        return "incorrect password"
@app.route("/login/")
def login():
    choice = request.args.get("choice")
    if choice =="1":
        a= render_template("credits.html")
        return a
    elif choice =="2":
        a= render_template("debit.html")
        return a
    elif choice=="3":
        account=session.get("data")
        account=account[0:4]
        file =open("bank_data\\"+account +".txt","r" )
        transactions =file.read()
        total=transactions.split("\n")
        a= render_template("balance.html",total=total)
        return a
    elif choice =="4":
        a= render_template("logout.html")
        return a
    else:
        a=render_template("bankapplication.html")
        return a
    return f"""{choice}"""
@app.route("/gateway")
def home():
    choice = request.args.get("choice")
    if choice =="1":
        a= render_template("login.html")
        return a
    elif choice =="2":
        a= render_template("signup.html")
        return a
    elif choice=="3":

        return"""
        
        <font size ="100">Thank You</font>


        """
    else:
        a=render_template("logout.html")
        return a
@app.route("/update",methods=[ "POST", "GET"])
def update():
    pass1 = request.args.get("pass1")
    pass2 = request.args.get("pass2")
    if pass1 == pass2 and len(pass1)>=8:
        data= session.get("data")
        data=session.get('data')
        file=open("record.txt","r")
        newdata=data.split(" ")
        newdata[5]=pass2
        newdata=" ".join(newdata)
        record=file.read()
        file.close()
        record=record.replace(data,newdata,)
        file=open("record.txt","w")
        file.write(record)
        file.close()
        session["data"]=newdata
        a= render_template("logout.html")
        return a
    else:
        """<center style = "color: red;">Password Doesn'match!
            <br> <a href="/otp.html>Try Again!</a>
        </center>
                <br>
                <a href="/logout.html>Home</a>"""
@app.route("/check",methods =['GET','POST'])
def check():
    account =request.form["account"]
    password  =request.form["password"]
    record=open("record.txt","r")
    data=record.read()
    record.close()
    data= data.split("\n")
    for i in data:
        if account in i[0:4]:
            if password in i and password == i.split(" ")[5]:
                session["data"]=i
                a= render_template("bankapplication.html")
                return a
            else:
                return "incorrect password"
    else:
        return"""Record not found"""
if __name__== "__main__":
    app.run(debug =True)
