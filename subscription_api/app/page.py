def html_page(config_key: str) -> str:
    html_content = f"""
            <html lang="ru">
                <head>
                    <meta charset="UTF-8">
                    <title>REVOLT VPN</title>
                </head>
                <body>
                    <h1>Ваши ключи для V2Ray:</h1>
                    <pre>{config_key}</pre>
                </body>
            </html>
            """
    return html_content