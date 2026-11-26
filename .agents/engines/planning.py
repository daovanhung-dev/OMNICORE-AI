def order(targets):
    visited=set(); active=set(); result=[]
    def visit(key):
        if key not in targets:raise ValueError('Thiếu target phụ thuộc: '+key)
        if key in active:raise ValueError('Phụ thuộc vòng tròn: '+key)
        if key in visited:return
        active.add(key)
        for dep in targets[key]['deps']:visit(dep)
        active.remove(key);visited.add(key);result.append(key)
    for key in targets:visit(key)
    return result
