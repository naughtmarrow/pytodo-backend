install:
	@poetry install

run:
	@flask --app src.main run

run-hosted:
	@gunicorn -w 4 'src.main:create_app()'
