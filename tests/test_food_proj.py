from food_proj import __version__

#TEST CAN BE RUN BY TYPING THE FOLLOWING COMMAND IN THE TERMINAL:
#python manage.py test

def test_version():
    assert __version__ == '0.1.0'
