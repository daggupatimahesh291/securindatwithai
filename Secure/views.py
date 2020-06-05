from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
import pymysql
from django.http import HttpResponse
import datetime
import json
import time
from hashlib import sha256


class Blockchain:
    # difficulty of our PoW algorithm
    difficulty = 2

    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        A function to generate genesis block and appends it to
        the chain. The block has index 0, previous_hash as 0, and
        a valid hash.
        """
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def add_block(self, block, proof):
        """
        A function that adds the block to the chain after verification.
        Verification includes:
        * Checking if the proof is valid.
        * The previous_hash referred in the block and the hash of latest block
          in the chain match.
        """
        previous_hash = self.last_block.hash

        if previous_hash != block.previous_hash:
            return False

        if not self.is_valid_proof(block, proof):
            return False

        block.hash = proof
        print("main "+str(block.hash))
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
        """
        Check if block_hash is valid hash of block and satisfies
        the difficulty criteria.
        """
        print("compare "+str(block_hash == block.compute_hash())+" "+block.compute_hash()+" "+str(block_hash.startswith('0' * Blockchain.difficulty)))
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.compute_hash())

    def proof_of_work(self, block):
        """
        Function that tries different values of nonce to get a hash
        that satisfies our difficulty criteria.
        """
        block.nonce = 0

        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def mine(self):
        """
        This function serves as an interface to add the pending
        transactions to the blockchain by adding them to the block
        and figuring out Proof Of Work.
        """
        if not self.unconfirmed_transactions:
            return False

        last_block = self.last_block

        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)

        self.unconfirmed_transactions = []
        return proof


class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0

    def compute_hash(self):
        """
        A function that return the hash of the block contents.
        """
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()

def AccessData(request):
    if request.method == 'GET':
       return render(request, 'AccessData.html', {})	

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def CreateProfile(request):
    if request.method == 'GET':
       return render(request, 'CreateProfile.html', {})

def Hospital(request):
    if request.method == 'GET':
       return render(request, 'Hospital.html', {})
def edit1(request):
    if request.method == 'GET':
       return render(request, 'edit1.html', {})

def Patient(request):
    if request.method == 'GET':
       return render(request, 'Patient.html', {})
def PatientDetails(request):
    user = ''
    with open("session.txt", "r") as file:
        for line in file:
           user = line.strip('\n')
    strdata = '<table border=1 align=center width=100%><tr><th>Patient ID</th><th>Patient Name</th><th>Age</th><th>Problem Description</th><th>Profile Date</th><th>Access Control</th><th>Gender</th><th>Contact No</th><th>Address</th><th>Block Chain Hashcode</th><th>Revenue</th></th></tr><tr>'
    con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'mahesh', database = 'SecuringData',charset='utf8')
    with con:
        cur = con.cursor()
        cur.execute("select * FROM patients where access_data like '%"+user+"%'")
        rows = cur.fetchall()
        for row in rows:

            strdata+='<td>'+str(row[0])+'</td><td>'+row[1]+'</td><td>'+str(row[2])+'</td><td>'+str(row[3])+'</td><td>'+str(row[4])+'</td><td>'+row[5]+'</td><td>'+row[6]+'</td><td>'+row[7]+'</td><td>'+row[8]+'</td><td>'+row[9]+'</td><td>'+str(row[10])+'</td></tr><tr>'
        context= {'data':strdata}

    return render(request,'PatientDetails.html',context)

def PatientLogin(request):
    if request.method == 'POST':
      pid = request.POST.get('t1', False)
      password = request.POST.get('t2', False)
      q=""
      s=""
      strdata = '<table border=1 align=center width=100%><tr><th>Patient ID</th><th>Patient Name</th><th>Age</th><th>Problem Description</th><th>Profile Date</th><th>Access Control</th><th>Gender</th><th>Contact No</th><th>Address</th><th>Block Chain Hashcode</th><th>Revenue</th><th>Password</th><th>Edit Details</th></th></tr><tr>'
      con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'mahesh', database = 'SecuringData',charset='utf8')
      with con:
          cur = con.cursor()
          cur.execute("select * FROM patients")
          rows = cur.fetchall()
          for row in rows:
             if str(row[0]) == pid:
                   q=str(row[0])
                   s=row[11]
                   strdata+='<td>'+str(row[0])+'</td><td>'+row[1]+'</td><td>'+str(row[2])+'</td><td>'+str(row[3])+'</td><td>'+str(row[4])+'</td><td>'+row[5]+'</td><td>'+row[6]+'</td><td>'+row[7]+'</td><td>'+row[8]+'</td><td>'+row[9]+'</td><td>'+str(row[10])+'</td><td>'+str(row[11])+'</td><td><button value='+str(row[0])+' name="t1">Edit</button></td>/tr><tr>'
    context= {'data':strdata}
    if(pid==q and password==s):
      return render(request, 'ViewData.html', context)
    else:
      return render(request, 'Patient.html', {})

def HospitalLogin(request):
    if request.method == 'POST':
      username = request.POST.get('t1', False)
      password = request.POST.get('t2', False)
      file = open('session.txt','w')
      file.write(username)
      file.close()   
      if username == 'Hospital1' and password == 'Hospital1' or username == 'Hospital2' and password == 'Hospital2':
       context= {'data':'welcome '+username}
       return render(request, 'HospitalScreen.html', context)
      else:
       context= {'data':'login failed'}
       return render(request, 'Hospital.html', context)

def updateRevenue(value):
    db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'mahesh', database = 'SecuringData',charset='utf8')
    db_cursor = db_connection.cursor()
    db_cursor.execute("update patients set revenue=revenue+0.5 where patient_id='"+value+"'")
    db_connection.commit()     

def PatientDataAccess(request):
    if request.method == 'POST':
      search = request.POST.get('t1', False)
      user = ''
      with open("session.txt", "r") as file:
          for line in file:
             user = line.strip('\n')
      strdata = '<table border=1 align=center width=100%><tr><th>Patient ID</th><th>Patient Name</th><th>Age</th><th>Problem Description</th><th>Profile Date</th><th>Access Control</th><th>Gender</th><th>Contact No</th></th></tr><tr>'
      con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'mahesh', database = 'SecuringData',charset='utf8')
      print("select * FROM patients where problem_desc like '%"+search+"%'")
      with con:
          cur = con.cursor()
          cur.execute("select * FROM patients where problem_desc like '%"+search+"%'")
          rows = cur.fetchall()
          for row in rows: 
             arr = row[5].split(" ")
             if len(arr) == 1:
                if arr[0] == user:
                   updateRevenue(str(row[0]))
                   strdata+='<td>'+str(row[0])+'</td><td>'+row[1]+'</td><td>'+str(row[2])+'</td><td>'+str(row[3])+'</td><td>'+str(row[4])+'</td><td>'+row[5]+'</td><td>'+row[6]+'</td><td>'+row[7]+'</td></tr><tr>'
             if len(arr) == 2:
                if arr[0] == user or arr[1] == user:
                   updateRevenue(str(row[0]))
                   strdata+='<td>'+str(row[0])+'</td><td>'+row[1]+'</td><td>'+str(row[2])+'</td><td>'+str(row[3])+'</td><td>'+str(row[4])+'</td><td>'+row[5]+'</td><td>'+row[6]+'</td><td>'+row[7]+'</td></tr><tr>'
    context= {'data':strdata}
    return render(request, 'ViewAccessData.html', context)
       

def CreateProfileData(request):
    if request.method == 'POST':
      name = request.POST.get('t1', False)
      age = request.POST.get('t2', False)
      problem = request.POST.get('t3', False)
      access_list = request.POST.getlist('t4', False)
      gender = request.POST.get('t5', False)
      contact = request.POST.get('t6', False)
      address = request.POST.get('t7', False)
      password = request.POST.get('t8', False)
      revenue = 0
      count = 0
      access = ''
      for i in range(len(access_list)):
         access+=access_list[i]+" "
      access = access.strip()
      db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'mahesh', database = 'SecuringData',charset='utf8')
      with db_connection:
          cur = db_connection.cursor()
          cur.execute("select count(*) FROM patients")
          rows = cur.fetchall()
          for row in rows:
            count = row[0]
      count = count + 1
      now = datetime.datetime.now()
      current_time = now.strftime("%Y-%m-%d %H:%M:%S")

      blockchain = Blockchain()
      x =  '{ "Patient_id":"'+str(count)+'", "patient_name":"'+name+'", "age":"'+age+'", "problem_desc":"'+problem+'", "profile_date":"'+str(current_time)+'", "access_data":"'+str(access)+'","gender":"'+gender+'"}'
      blockchain.add_new_transaction(json.loads(x))
      hash = blockchain.mine()

      db_cursor = db_connection.cursor()
      student_sql_query = "INSERT INTO patients(Patient_id,patient_name,age,problem_desc,profile_date,access_data,gender,contact_no,address,blockchain_hash,revenue,password) VALUES('"+str(count)+"','"+name+"','"+age+"','"+problem+"','"+current_time+"','"+str(access)+"','"+gender+"','"+contact+"','"+address+"','"+hash+"','"+str(revenue)+"','"+str(password)+"')"
      db_cursor.execute(student_sql_query)
      db_connection.commit()
      print(db_cursor.rowcount, "Record Inserted")
      if db_cursor.rowcount == 1:
       context= {'data':'Profile Creation Process Completed. Your Patient ID : '+str(count)}
       return render(request, 'CreateProfile.html', context)
      else:
       context= {'data':'Error in profile creation process'}
       return render(request, 'CreateProfile.html', context)
def edit(request):
    if request.method == 'POST':
          pid = request.POST.get('t1', False)

          strdata=''
          con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'mahesh', database = 'SecuringData',charset='utf8')
          with con:
              cur = con.cursor()
              cur.execute("select * FROM patients")
              rows = cur.fetchall()
              for row in rows:
                 if str(row[0]) == pid:
                   b=row[3].split(' ')
                   d=row[8].split(' ')
                   a=""
                   for i in b:
                     a+=i
                   c=""
                   for i in d:
                     c+=i
                   strdata='<tr><td><b>Patient&nbsp;Id</b></td><td><input type="text"  value='+str(row[0])+' name="t0" style="font-family: Comic Sans MS" size="30" readonly></td></tr><tr><td><b>Patient&nbsp;Name</b></td><td><input type="text" name="t1" value='+row[1]+' style="font-family: Comic Sans MS" size="30"></td></tr><tr><td><b>Age</b></td><td><input  type="Text" value='+str(row[2])+' name="t2"size="10"></td></tr><tr><td><b>Problem&nbsp;Desc</b></td><td><textarea name="t3" rows="10" placeholder='+a+' cols="60" ></textarea></td></tr><tr><td><b>Access Control</b></td><td><select name="t4" multiple><option value="Hospital1">Hospital 1</option><option value="Hospital2">Hospital 2</option></select></td></tr><tr><td><b>Gender</b></td><td><select name="t5" style="font-family: Comic Sans MS"><option value="Male">Male</option><option value="Female">Female</option></select></td></tr><tr><td><b>Contact&nbsp;No</b></td><td><input type="text" value='+str(row[7])+' name="t6" style="font-family: Comic Sans MS" size=20/></td></tr><tr><td><b>address</b></td><td><textarea name="t7" placeholder='+c+' style="font-family: Comic Sans MS" rows="6" cols="30"></textarea></td></tr><tr><td><b>Password</b></td><td><input type="text" name="t8" value='+str(row[11])+' style="font-family: Comic Sans MS" size="20"></td></tr>'

    context= {'data':strdata}
    return render(request, 'edit1.html', context)
def update(request):
    if request.method == 'POST':
      id = request.POST.get('t0', False)
      name = request.POST.get('t1', False)
      age = request.POST.get('t2', False)
      problem = request.POST.get('t3', False)
      access_list = request.POST.getlist('t4', False)
      gender = request.POST.get('t5', False)
      contact = request.POST.get('t6', False)
      address = request.POST.get('t7', False)
      pa = request.POST.get('t8', False)
      revenue=0
      count = 0
      access = ''
      for i in range(len(access_list)):
         access+=access_list[i]+" "
      access = access.strip()
      db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'mahesh', database = 'SecuringData',charset='utf8')
      with db_connection:
          cur = db_connection.cursor()
          cur.execute("select count(*) FROM patients")
          rows = cur.fetchall()
          for row in rows:
            count = row[0]
      count = count + 1
      now = datetime.datetime.now()
      current_time = now.strftime("%Y-%m-%d %H:%M:%S")

      blockchain = Blockchain()
      x =  '{ "Patient_id":"'+str(count)+'", "patient_name":"'+name+'", "age":"'+age+'", "problem_desc":"'+problem+'", "profile_date":"'+str(current_time)+'", "access_data":"'+str(access)+'","gender":"'+gender+'"}'
      blockchain.add_new_transaction(json.loads(x))
      hash = blockchain.mine()

      db_cursor = db_connection.cursor()
      student_sql_query = """UPDATE patients SET patient_name= %s,age= %s,problem_desc= %s,profile_date= %s,access_data= %s,gender= %s,contact_no= %s,address= %s,blockchain_hash=%s,password= %s where Patient_id= %s"""
      input=(name,int(age),problem,current_time,str(access),str(gender),contact,address,hash,pa,int(id))
      db_cursor.execute(student_sql_query,input)
      #db_cursor.execute('''UPDATE patients SET patient_name=name,age=age,problem_desc=problem,access_data=str(access)+,contact_no=contact,address=address),blockchain_hash=str(hash),password=password where Patient_id=int(id)''')
      db_connection.commit()
      print(db_cursor.rowcount, "Record Inserted")
      if db_cursor.rowcount == 1:
       context= {'data':'Profile Updation Process Completed. Your Patient ID : '+str(id)}
       return render(request, 'ViewData.html', context)
      else:
       context= {'data':'Error in Updation creation process'}
       return render(request, 'ViewData.html', context)








