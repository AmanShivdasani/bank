from flask import Flask,render_template,request,session,url_for
app =Flask(__name__,template_folder='templates',static_folder= 'static')
app.config['SECRET_KEY']="1234567890"
#landing page
@app.route("/logout")
def logout():
    """This takes us to the landing page of the website"""
    session["data"]="guest"
    a=render_template("logout.html")
    return a
#redirection to choosen page
@app.route("/gateway")
def home():
    """it checks the option selected by user and take the user selected action"""
    choice = request.args.get("choice")
    if choice =="1":
        a= render_template("login.html")
        return a
    elif choice =="2":
        a= render_template("signup.html")
        return a
    elif choice=="3":
        return render_template("Exit.html")   
    else:
        a=render_template("logout.html")
        return a
#if choosen login 

#login page
@app.route("/bank")
def bank():
    a=render_template("bankapplication.html")
    return a
#redirection to choosen page
@app.route("/debit")
def debit():
    """This takes us to the debit page of the website"""
    a=render_template("debit.html")
    return a
@app.route("/credit")
def credit():
    """This takes us to the credit page of the website"""
    a=render_template("credits.html")
    return a
@app.route("/balance")
def balance():
    """This takes us to the transaction page of the website"""
    account=session.get("data")
    account=account[0:4]
    file =open("bank_data\\"+account +".txt","r" )
    transactions =file.read()
    total=transactions.split("\n")
    a= render_template("balance.html",total=total)
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
        if len(account)>=1 and len(contact)==10 and account in i[0:4]:
            if contact in i and contact== i.split(" ")[3]:
                session["data"]=i
                a= render_template("otp.html")
                return a
            else:
                return render_template("forgot.html",diff ="Contact Doesn't match!")

    return render_template("forgot.html",diff ="No record found!")

@app.route("/forgot")
def forgot():
    return render_template("forgot.html")

@app.route("/amount_reduce")
def amount_reduce():
    amount= request.args.get("amount")
    balance=session.get("data").split(" ")[4]
    if amount==""or int(amount) > int(balance):
        return render_template("debit.html",diff="Insufficient balance")
    elif int(amount) <=0:
        return render_template("debit.html",diff="minimum Transaction is \u20B9 1")
    else:
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
    if amount =="" or int(amount)>0:
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
    else:
        a=render_template("credits.html",diff="Minimum amount is rupees 1")
        return a
@app.route("/verify", methods =["GET","Post"])
def verify():
    f_name = request.args.get("f_name")
    l_name = request.args.get("l_name")
    email = request.args.get("emaill")
    balance = request.args.get("balance")
    contact =request.args.get("contact")
    pass1 = request.args.get("pass1")
    pass2 = request.args.get("pass2")
    if pass1 == pass2 and len(pass1)>=8 and f_name != "" and l_name != "" and len(contact)==10 and email !="":
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
        return render_template("account.html",account=num)
    else:
        return render_template("signup.html",diff="Please Enter correct details")
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
    elif len(pass1)>=8 and len(pass2)>=8:
        return render_template("otp.html", diff="Password doesn't match")
    else:
        return render_template("otp.html", diff="Please enter valid password ")
        
@app.route("/check",methods =['GET','POST'])
def check():
    account =request.form["account"]
    password  =request.form["password"]
    record=open("record.txt","r")
    data=record.read()
    record.close()
    data= data.split("\n")
    for i in data:
        if len(account)>=1 and account in i[0:4]:
            if password in i and password == i.split(" ")[5]:
                session["data"]=i
                a= render_template("bankapplication.html")
                return a
            else:
                return render_template("login.html",diff="Incorrect password")
    else:
        return render_template("login.html",diff="""Record not found""")
@app.route("/feedback")
def feedback():
    return render_template("feedback.html")
@app.route("/store",methods=["GET","Post"])
def store():
    feedback= request.args.get("feedback")
    if feedback != None:
        account =session.get("data").split(" ")[0]
        feedback= account + ":" + feedback +"\n"
        record=open("feedback.txt","a")
        record.write(feedback)
        record.close()
        return render_template("login.html")
    else:
        return render_template("login.html")
@app.route("/interest",methods=["GEt","PUT"])
def interest():
    return render_template("interest.html")
@app.route("/calc",methods=["get","post"])
def calc():
    amount=request.args.get("amount")
    year=request.args.get("year")
    month=request.args.get("month")
    if amount.isdigit() and year.isdigit() and month.isdigit() and int(amount)>0 and int(month)+int(year)>=1:
        amount,year,month=int(amount),int(year),int(month)
        time =year *12 +month
        if time <=12:
            interest =amount + 8*amount/100
        elif time <=60:
            interest =amount + 10*amount/100
        elif time <=120:
            interest =amount + 15*amount/100
        else:
            interest =amount + 20*amount/100
        return render_template("interest.html",diff = f"The interest for {year} year and {month} month is \u20B9 {interest}.")
    else:
        return render_template("interest.html",diff="Please Enter Correct Details")
@app.route("/transfer",methods = ["GET","POST"])
def transfer():
    return render_template("transfer.html")
@app.route("/transaction",methods=["get","POST"])
def transaction():
    mine=session.get("data")
    account =request.form["account"]
    amount =request.form["amount"]
    password=request.form["pass"]
    balance=session.get("data").split(" ")[4]
    if password == mine.split(" ")[5]:
        record=open("record.txt","r")
        data=record.read()
        record.close()
        data= data.split("\n")
        for i in data:
            if len(account)>=1 and account in i[0:4]:
                    if amount==""or int(amount) > int(balance) :
                        return render_template("transfer.html",diff="Insufficient balance")
                    elif int(amount) <=0:
                        return render_template(".html",diff="minimum Transaction is \u20B9 1")
                    else:
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
                        session["data"]= i
                        data=session.get("data")
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
                        session["data"]= mine
                        a=render_template("amount.html",amount=amount)
                        return a
                
        else:
            return render_template("transfer.html",diff="No Account Exist")
    else:
        return render_template("transfer.html",diff="Incorrect password")


        
if __name__== "__main__":
    app.run(host ="0.0.0.0",debug=True)
