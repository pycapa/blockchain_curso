# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 14:43:44 2022

@author: carlos
"""

# Modulo 1: Crear un blockchain

# Importar las Librerias

import datetime
import hashlib
import json
from urllib import response
from flask import Flask, jsonify, render_template

## Crear la cadena de bloques. ##

class Blockchain:
    def __init__(self): #referencia al objeto que estamos creando
        self.chain = [] # Contendra todos los bloques de la cadena.
        self.create_block(proof = 1, previous_hash = '0', hash='0') # proof: Identificador del bloque
        
    ## Funcion create_block
    def create_block(self, proof, previous_hash, hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp' : str(datetime.datetime.now()),
            'proof' : proof,
            'previous_hash': previous_hash,
            'hash' : hash}

        self.chain.append(block)
        return block
    
    ## Obtener el bloque previo
    def get_previous_block(self):
        return self.chain[-1]
    
    ## Prueba de trabajo, para generar el nuevo problema requerimos la utilma solucion hallada.
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while not check_proof:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                print(hash_operation)
                check_proof = True
            else:
                new_proof += 1
        return new_proof, hash_operation         
        
    ## Buscar el hash del bloque
    def hash(self, block):
        encode_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encode_block).hexdigest()
                 
    ## Comprobar que la cadena es valida.
    def is_chain_valid(self, chain):
        # Bloque previo
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            # comprobar el vinculo de los hashs
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            # validar la operacion para las primeras 4 posiciones.
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
    
## Minado de un bloque de la cadena. ##


# 1. Applicacion Web (webapp)

app = Flask(__name__)

# 1. Crear una blockchain
blockchain = Blockchain()

# 2. Crear una cadena de bloques.
@app.route('/')
def index():
    return render_template('index.html', data={'message':'You are in a blockchain app.'}, response=200)

@app.route('/mineblock', methods=['GET'])
def mineblock():
    # bloque previo
    previous_block = blockchain.get_previous_block()
    # prueba de trabajo del bloque previo
    previous_proof = previous_block['proof']
    proof, hash = blockchain.proof_of_work(previous_proof)
    # hash previo
    #previous_hash = blockchain.hash(previous_block)
    print(hash)
    block = blockchain.create_block(proof, previous_block['hash'], hash)
    response = { 'message':'Excelente, has minado un nuevo bloque',
                 'index': block['index'],
                 'timestamp' : block['timestamp'],
                 'proof' : block['proof'],
                 'previous_hash' : block['previous_hash'],
                 'hash': block['hash']}
    return response, 200

@app.route('/get_chain', methods=['GET'])
def get_chain():
    response =  {'chain': blockchain.chain,
                 'lenght':len(blockchain.chain)}
    return response, 200


@app.route('/last_block', methods=['GET'])
def last_block():
    block = blockchain.get_previous_block()
    response = { 'message':'El ultimo bloque contiene:',
                 'index': block['index'],
                 'timestamp' : block['timestamp'],
                 'proof' : block['proof'],
                 'previous_hash': block['previous_hash'],
                 'hash' : block['hash']}
    return response
    
#Ejecutar la app
app.run(host = '0.0.0.0', port=5000, debug=True)






