from flask import Flask
from flask_cors import CORS, cross_origin
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.options import WebpayOptions
from transbank.common.integration_type import IntegrationType
from transbank.error.transbank_error import TransbankError

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})