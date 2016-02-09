# jupyter-wheel


Wheel
======

The wheel is a circler set of clickable cells designed to operate as an IRMA (Interactive Reconfigurable Matrix of Alteritives) or as a capability wheel. 


Basic Use
======

    
    from wheel import *
    
    f = open("demo.json")
    data = f.read()
    f.close
    
    Wheel(value=data)
