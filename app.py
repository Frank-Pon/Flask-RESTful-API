from flask import Flask,request,jsonify

app = Flask(__name__)
products = [
    {"id": 1, "name": "Apple iPhone 14"},
    {"id": 2, "name": "Samsung Galaxy S22"},
    {"id": 3, "name": "Google Pixel 7"},
    {"id": 4, "name": "Apple MacBook Pro"},
    {"id": 5, "name": "ASUS ZenBook"}
]

@app.route('/')
def home():
    return jsonify({'message':'測試成功'})

@app.route('/search')
def find():
    kw = request.args.get('name','') #設定變數裝品名參數
    pid = request.args.get('id','') #設定變數裝id參數
    result = [p for p in products if p['name'].lower().startswith(kw.lower()) and (str(p['id']) == pid if pid else True)]
    #找出符合條件的裝進result
    if not result: #如果沒有資料回傳找不到資料
        return jsonify({'message':'找不到資料'})
    return jsonify(result) #有的話就回傳result

@app.route('/add',methods=['POST'])
def prod_add():
    data = request.get_json() #將接收到的請求變成json裝在data
    if not data or 'name' not in data or 'id' not in data:
    #如果沒有資料或資料錯誤
        return jsonify({'message':'請確認品名及ID是否正確'})
        #回傳錯誤訊息
    products.append({
        'name':data['name'],
        'id':data['id']
    })#如果有資料且資料無誤,將回傳的資料加進列表
    
    return jsonify({'message':f'品名 {data['name']} ID {data['id']}的資料已新增'})
    #回傳成功訊息

@app.route('/del/<int:pid>',methods=['DELETE'])
def prod_del(pid):
    product = next((p for p in products if p['id'] == pid),None)
    #找出符合條件的資料
    if not product:#若無資料回傳錯誤訊息
        return jsonify({'message':f'查無ID為 {pid} 的資料'})
    #有資料則刪除
    products.remove(product)
    return jsonify({'message':f'商品 {product['name']}已刪除'})
    #回傳成功訊息

@app.route('/put/<int:pid>',methods=['PUT'])
def prod_put(pid):
    data = request.get_json() #接收傳送過來的請求變成json格式存放在data
    if not data or 'name' not in data: #如果沒資料或是沒商品給出錯誤訊息
        return jsonify({'message':'請確認變更資料正確'})
    product = next((p for p in products if p['id'] == pid),None)
    #找出對應ID的位置
    product['name'] = data['name']
    #更換商品
    return jsonify({'message':f'ID {pid} 的商品已更改完成'})
    #回傳成功訊息

app.run(debug=True)

'''
回傳的資料型態
[
  {
    "id": 1,
    "name": "Apple iPhone 14"
  },
  {
    "id": 4,
    "name": "Apple MacBook Pro"
  }
]
'''