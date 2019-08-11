# api-farms

Simple API In Python.

### Pre Requisits

1. Setup and install[MongoDB Community Server](https://www.mongodb.com/download-center/community)

2. Install pip requirements
```
pip install -r requirements.txt
```

### Setup

#### **WITH MAKE**

1. Build
```
make build
```

2. Install
```
make install
```

#### **WITHOUT MAKE**

1. Build
```
python setup.py build
```

2. Install
```
python setup.py install
```

### Run API/Server

1. Run the main Flask application
```
python farm/app.py
```

### Testing

1. Run the testing script
```
python farm/test_app.py
```
