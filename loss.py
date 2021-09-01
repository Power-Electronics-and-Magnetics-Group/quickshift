from main import current_sharing
import sympy as sp 
F = current_sharing(8,[2,3,4,7])

def loss(ff):
    loss_sum=0
    for term in ff:
        loss_sum = loss_sum + term**2 
        return loss_sum
Ip=sp.symbols("Ip")
x=loss(F).coeff(Ip**2)
print(x)
