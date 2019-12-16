def search_fn(token, query_str):
    return {
        'messages' : [
            'Hello ' + token + ' ' + query_str,
            # Not the right structure
        ]
    }
