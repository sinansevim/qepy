def check_relax(path):
    lines = open(path, 'r').readlines()
    for i in lines:
        if "bfgs failed after" in i:
            return False
        if "bfgs converged" in i:
            return True