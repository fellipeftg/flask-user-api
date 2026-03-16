from app import create_app

app = create_app()  # Aqui a aplicação Flask é criada chamando a função create_app()

if __name__ == "__main__":  # Executa o código abaixo apenas se este arquivo for executado diretamente
    app.run(debug=True)  # Inicia o servidor de desenvolvimento do Flask
    # API disponível em http://127.0.0.1:5000