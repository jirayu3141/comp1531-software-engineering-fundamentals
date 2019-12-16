def foo(zid=None, name=None, *args, **kwargs):
    print(zid, name)
    print(args) # A list
    print(kwargs) # A dictionary

if __name__ == '__main__':
    
    foo('z3418003', None, 'mercury', 'venus', 'list_item', planet1='earth', planet2='mars', users= 'user3')