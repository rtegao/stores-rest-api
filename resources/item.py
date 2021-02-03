from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.item import ItemModel

class Item(Resource):
    # paser belongs to the class Item, to use parse it's necessary Item.parse
    parse = reqparse.RequestParser()
    parse.add_argument(
        'price',
        type = float,
        required = True,
        help = "This field cannot beleft blank"
        )

    parse.add_argument(
        'store_id',
        type = float,
        required = True,
        help = "Every item need a store id."
        )

    # @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()       
        return {"message":"Item not found"},404 

    def post(self,name):
        if  ItemModel.find_by_name(name):
            return {'message' : f"an item with name '{name}' already exist"}, 400 #400 bad request status code
        data = Item.parse.parse_args() #reading data send by the browser 
        item = ItemModel(name,**data)
        try:
            item.save_to_db()
        except:
            return{"message":"An error occured inserting the item."},500 #500 internal server error status code
        return item.json(), 201 #201 created, status code

    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message':'Item deleted'},200
        return {'message':'Item not found'},400
        
    # @jwt_required()
    def put(self,name): #can be use for create or update items
        data = Item.parse.parse_args() #reading data send by the browser 
        item = ItemModel.find_by_name(name)
        if item:
            try:
                item.price = data['price']
            except:
                return {"message","An error occured updating the item"}, 500 #internal server error status code
        else:
            try:
                item = ItemModel(name,**data)
            except:
                return {"message","An error occured inserting the item"}, 500 #internal server error status code        
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {"items": list(map(lambda x: x.json(), ItemModel.query.all()))},200 #200 good request, status code