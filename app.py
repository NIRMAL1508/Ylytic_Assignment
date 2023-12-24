import json
from flask import Flask, request, jsonify
from datetime import datetime
import logging 
logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)

# Assuming the existing API endpoint
BASE_URL = "https://app.ylytic.com/ylytic/test"

# Load comments data from a separate file
with open("comments_data.json", "r") as file:
    comments_data = json.load(file)

# Helper function to filter comments based on search criteria
def filter_comments(comments, filters):
    filtered_comments = comments
    
    # Filter by search text
    if "search_text" in filters:
        text_query = filters["search_text"].lower()
        filtered_comments = [c for c in filtered_comments if text_query in c["text"].lower()]

    # Filter by author name
    if "search_author" in filters:
        author_query = filters["search_author"].lower()
        filtered_comments = [c for c in filtered_comments if author_query in c["author"].lower()]

    # Filter by date range
    if "at_from" in filters and "at_to" in filters:
        from_date = datetime.strptime(filters["at_from"], "%d-%m-%Y")
        
        to_date = datetime.strptime(filters["at_to"],  "%d-%m-%Y")

        filtered_comments = [c for c in filtered_comments if from_date <= datetime.strptime(c["at"], "%a, %d %b %Y %H:%M:%S GMT") <= to_date]

    # Filter by like and reply count range
    # for field in ["like_from", "like_to", "reply_from", "reply_to"]:
    #     if field in filters:
    #         # Check if the field exists before accessing it
    #         filtered_comments = [c for c in filtered_comments if field[:-5] in c and c[field[:-5]] is not None and int(filters[field]) <= int(c[field[:-5]]) <= int(filters[field[:-3]])]

    if "like_from" and "like_to" in filters:
        likefrom = filters["like_from"]
        liketo = filters["like_to"]
        filtered_comments = [c for c in filtered_comments if int(likefrom) <= int(c["like"]) <= int(liketo)] 
    
    if "reply_from" and "reply_to" in filters:
        replyfrom = filters["reply_from"]
        replyto = filters["reply_to"]
        filtered_comments = [c for c in filtered_comments if int(replyfrom) <= int(c["reply"]) <= int(replyto)] 

    return filtered_comments

# Search API endpoint
@app.route('/search', methods=['GET'])
def search_comments():
    try:
        filters = request.args.to_dict()
        filtered_comments = filter_comments(comments_data, filters)
        return jsonify({"comments": filtered_comments})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
