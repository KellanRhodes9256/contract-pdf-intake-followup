import run_contract


def test_main_prints_download_url(monkeypatch, capsys):
    monkeypatch.setenv("INFRAI_API_KEY", "test-key")
    monkeypatch.setattr(
        run_contract.InfraiPdfClient,
        "generate",
        lambda self, markdown: {"id": "pdf-7", "url": "https://files.example/pdf-7"},
    )

    run_contract.main()

    assert "'download_url': 'https://files.example/pdf-7'" in capsys.readouterr().out
