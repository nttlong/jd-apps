import routes
app =routes.app
app_config = routes.app_config
import routes.api_files


if __name__ == '__main__':
    app_config.logger.info("------------------------------------------------------")
    app_config.logger.info("web start with:")
    app_config.logger.info(dict(debug=app_config.debug, host=app_config.host, port=app_config.port))
    app_config.logger.info("------------------------------------------------------")
    app.run(
          debug=app_config.debug,
          host= app_config.host,
          port=app_config.port
    )



