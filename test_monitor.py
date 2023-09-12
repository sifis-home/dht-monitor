import json
from unittest.mock import patch

import pytest
import requests

from dht_monitor import catch_topic


def on_message(ws, message):
    print(
        "Received:"
    )  # Assicurati che questa riga sia presente come prima istruzione

    json_message = json.loads(message)

    if "Persistent" in json_message:
        json_message = json_message["Persistent"]

        print("\n\n")
        print("JSON-MESSAGE")
        print(json_message["topic_name"], json_message["topic_uuid"])
        # Send data to Flask server
        data = {
            "topic_name": json_message["topic_name"],
            "topic_uuid": json_message["topic_uuid"],
        }
        url = "http://localhost:4646/topic"
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("Data sent to Flask server")
        else:
            print("Failed to send data to Flask server")


# Funzione di test semplice per on_message
def test_on_message_simple():
    # Definire il messaggio JSON fittizio
    json_message = {
        "Persistent": {"topic_name": "test_topic", "topic_uuid": "12345"}
    }

    # Mock della richiesta HTTP per restituire uno stato 200
    with patch.object(requests, "post") as mock_post:
        mock_post.return_value.status_code = 200

        # Chiamare la funzione target
        catch_topic.on_message(None, json.dumps(json_message))

    # Non è necessario testare le chiamate a print in questo caso
    # Verificare che la richiesta HTTP sia stata chiamata con i dati corretti
    mock_post.assert_called_once_with(
        "http://localhost:4646/topic", json=json_message["Persistent"]
    )


# Funzione di test per on_error
def test_on_error():
    # Mock delle chiamate a print
    with patch("builtins.print") as mock_print:
        error_message = "Test error message"
        catch_topic.on_error(None, error_message)

        # Verificare che la funzione di stampa sia stata chiamata con il messaggio di errore corretto
        mock_print.assert_called_once_with(error_message)


# Funzione di test per on_close
def test_on_close():
    # Mock delle chiamate a print
    with patch("builtins.print") as mock_print:
        close_status_code = 1000
        close_msg = "Connection closed"
        catch_topic.on_close(None, close_status_code, close_msg)

        # Verificare che la funzione di stampa sia stata chiamata con i parametri di chiusura corretti
        mock_print.assert_called_once_with("### Connection closed ###")


# Funzione di test per on_open
def test_on_open():
    # Mock delle chiamate a print
    with patch("builtins.print") as mock_print:
        catch_topic.on_open(None)

        # Verificare che la funzione di stampa sia stata chiamata con il messaggio di connessione corretto
        mock_print.assert_called_once_with("### Connection established ###")


# Eseguire i test
if __name__ == "__main__":
    pytest.main()
