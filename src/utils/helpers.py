from flask import Flask, jsonify
import hashlib
ERROR_RESPONSE_STRING = 'SOMETHING WENT WRONG'
SUCCESS_RESPONSE_STRING = "PROCESSED SUCCESSFULLY"

def getErrResponse (error):
    return jsonify({
        'error': error
    }),  503

def getSuccessResponse (data):
    return data,200

def getHash(string: str):
    return hashlib.sha256(string.encode()).hexdigest()