from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect


# Create your views here.

def login_home(request):
    return render(request,'login_home.html')

def login(request):
    if request.method == 'POST':
        idname = request.POST['name']
        password = request.POST['password']
        print(idname,password)

        cursor = connection.cursor()
        cursor.execute("select * from login where admin_id = '"+str(idname)+"' and password = '"+str(password)+"'")
        admin = cursor.fetchone()

        if admin == None:
            return HttpResponse("<script>alert('invalid login');window.location='../login';</script>")

        else:
            request.session["adminid"] = idname
            return redirect('adminindex')
    else:
        return render(request,'login.html')


def logout(request):
    return redirect('loginhome')

def admin_home(request):
    return render(request,'electronics/index.html')
def add_category(request):
    if request.method == 'POST':
        name = request.POST['name']
        img_link = request.POST['img_link']
        # phone = request.POST['phone']
        # exp = request.POST['experience']
        cursor = connection.cursor()
        cursor.execute("insert into category values(null,'"+name+"','"+str(img_link)+"')")
        return redirect(add_category)
    else:
        return render(request,'electronics/add_category.html')

def view_category(request):
    cursor = connection.cursor()
    cursor.execute("select * from category ")
    data = cursor.fetchall()
    return render(request, 'electronics/view_category.html',{'data':data})


def add_items(request, id):
    if request.method == 'POST':
        company = request.POST['company']
        item_des = request.POST['item_des']
        year = request.POST['year']
        price = request.POST['price']
        imglink = request.POST['img_link']
        cursor = connection.cursor()
        cursor.execute("insert into item_details values(null,'"+str(id)+"','"+str(item_des)+"','"+str(year)+"','"+str(price)+"','"+str(company)+"','"+str(imglink)+"')")
        return redirect('add_items', id=id)
    else:
        return render(request,'electronics/add_items.html')

def view_items(request,id):
    cursor = connection.cursor()
    cursor.execute("select * from item_details where idcategory ='"+str(id)+"' ")
    data = cursor.fetchall()
    return render(request, 'electronics/view_items.html',{'data':data})

def edit_items(request, id):
    if request.method == 'POST':
        company = request.POST['company']
        item_des = request.POST['item_des']
        year = request.POST['year']
        price = request.POST['price']
        imglink = request.POST['img_link']
        cursor = connection.cursor()
        cursor.execute("update item_details set item_description ='"+str(item_des)+"', year ='"+str(year)+"', price ='"+str(price)+"', company ='"+str(company)+"', img_link ='"+str(imglink)+"' where item_id ='"+str(id)+"' ")
        return redirect(view_category)
    else:
        cursor = connection.cursor()
        cursor.execute("select * from item_details where item_id ='"+str(id)+"'")
        data = cursor.fetchone()
        return render(request,'electronics/edit_items.html',{'data':data})
def delete_items(request, id):
    cursor = connection.cursor()
    cursor.execute("delete from item_details where item_id ='"+str(id)+"' ")
    return redirect(view_category)
def payed_orders(request):
    cursor = connection.cursor()
    cursor.execute("select order_master.*, user_register.* from order_master join user_register where order_master.status ='paid' and order_master.user_id = user_register.user_id ")
    data = cursor.fetchall()
    return render(request, 'electronics/payed_orders.html',{'data':data})

def ship_item(request,id):
    cursor = connection.cursor()
    cursor.execute("update order_master set status = 'shipped' where idorder_master = '"+str(id)+"' ")
    return redirect(payed_orders)

def view_orders(request,id):
    cursor = connection.cursor()
    cursor.execute("select order_items.*, item_details.* from order_items join item_details where order_items.idorder_master ='"+str(id)+"' and order_items.item_id = item_details.item_id ")
    data= cursor.fetchall()
    return render(request, 'electronics/view_orders.html',{'data':data})

def shipped_orders(request):
    cursor = connection.cursor()
    cursor.execute("select order_master.*, user_register.* from order_master join user_register where order_master.status ='shipped' and order_master.user_id = user_register.user_id ")
    data = cursor.fetchall()
    return render(request, 'electronics/shipped_orders.html', {'data': data})

def return_requests(request):
    cursor = connection.cursor()
    cursor.execute("select item_return.*, item_details.*, user_register.*, order_master.* from item_return join item_details join user_register join order_master where item_return.status = 'pending' and item_return.user_id = user_register.user_id and item_return.item_id = item_details.item_id and order_master.idorder_master = item_return.idorder_master ")
    data = cursor.fetchall()
    return render(request, 'electronics/return_requests.html',{'data':data})
def approve_return(request,id):
    cursor = connection.cursor()
    cursor.execute("update item_return set status ='processing' where iditem_return ='"+str(id)+"' ")
    return redirect(return_requests)

def cancel_return(request,id):
    cursor = connection.cursor()
    cursor.execute("update item_return set status ='canceled' where iditem_return ='"+str(id)+"' ")
    return redirect(return_requests)

def return_approved(request):
    cursor = connection.cursor()
    cursor.execute("select item_return.*, item_details.*, user_register.*, order_master.* from item_return join item_details join user_register join order_master where item_return.status = 'processing' and item_return.user_id = user_register.user_id and item_return.item_id = item_details.item_id and order_master.idorder_master = item_return.idorder_master or item_return.status = 'shipped' and item_return.user_id = user_register.user_id and item_return.item_id = item_details.item_id and order_master.idorder_master = item_return.idorder_master ")
    data = cursor.fetchall()
    return render(request, 'electronics/return_approved.html',{'data':data})

def collect_return(request,id):
    cursor = connection.cursor()
    cursor.execute("update item_return set status ='shipped' where iditem_return ='"+str(id)+"' ")
    return redirect(return_approved)

def return_cancelled(request):
    cursor = connection.cursor()
    cursor.execute("select item_return.*, item_details.*, user_register.*, order_master.* from item_return join item_details join user_register join order_master where item_return.status = 'canceled' and item_return.user_id = user_register.user_id and item_return.item_id = item_details.item_id and order_master.idorder_master = item_return.idorder_master ")
    data = cursor.fetchall()
    return render(request, 'electronics/return_canceled.html', {'data': data})

def admin_logout(request):
    return render(request,'electronics/LogOut.html')
def view_feedback(request):
    cursor = connection.cursor()
    cursor.execute("select feedback.*,user_register.name from feedback join user_register where feedback.user_id =user_register.user_id ")
    data = cursor.fetchall()
    return render(request,'electronics/feedbacks.html',{'data':data})

def reply_feed(request, id):
    if request.method == 'POST':
        reply = request.POST['reply']
        cursor = connection.cursor()
        cursor.execute("update feedback set reply ='"+str(reply)+"' where id ='"+str(id)+"' ")
        return redirect(view_feedback)
    else:
        cursor = connection.cursor()
        cursor.execute("select feedback.*, user_register.name from feedback join user_register where feedback.id ='"+str(id)+"' and feedback.user_id =user_register.user_id")
        data = cursor.fetchone()
        return render(request,'electronics/reply_feed.html',{'data':data})


