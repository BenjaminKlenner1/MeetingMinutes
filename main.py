from website import create_app

app = create_app()
app.config['SECRET_KEY'] = 'KlEnNeR'

if __name__ == '__main__':
    app.run(debug=True)
    