#!/usr/bin/env python3
""" Log stats - new version """
from pymongo import MongoClient


def nginx_stats_check():
    """ provides some stats about Nginx logs stored in MongoDB:"""
    client = MongoClient()
    collection = client.logs.nginx

    num_of_docs = collection.count_documents({})
    print(f"{num_of_docs} logs")
    print("Methods:")
    methods_list = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods_list:
        method_count = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {method_count}")
    status = collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{status} status check")

    print("IPs:")

    top_IPs = collection.aggregate([
        {"$group":
         {
             "_id": "$ip",
             "count": {"$sum": 1}
         }
         },
        {"$sort": {"count": -1}},
        {"$limit": 10},
        {"$project": {
            "_id": 0,
            "ip": "$_id",
            "count": 1
        }}
    ])
    for top_ip in top_IPs:
        count = top_ip.get("count")
        ip_address = top_ip.get("ip")
        print(f"\t{ip_address}: {count}")


if __name__ == "__main__":
    nginx_stats_check()
