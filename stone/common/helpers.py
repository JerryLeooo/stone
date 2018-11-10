def convert(source, target):
    for k, v in filter(
        lambda item: not item[0].startswith("_") and not item[0] in source.__dict__.keys(),
        target.__dict__.items()
    ):
        print(k, v)
        setattr(source, k, v)
    
    return source