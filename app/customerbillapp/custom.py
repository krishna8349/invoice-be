

def errorMessage(code, reason, message, status, referenceerror, basetype, schemalocation, type):
    error = {}
    error['code'] = code
    error['reason'] = reason
    error['message'] = message
    error['status'] = status
    error['referenceError'] = referenceerror
    error['@baseType'] = basetype
    error['@schemaLocation'] = schemalocation
    error['@type'] = type
    return error

# create helper function to return error mess


