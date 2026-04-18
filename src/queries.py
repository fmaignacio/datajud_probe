def query_basica(size: int = 20) -> dict:
    return {
        "size": size,
        "query": {
            "bool": {
                "filter": [
                    {"term": {"nivelSigilo": 0}}
                ]
            }
        },
        "sort": [{"@timestamp": {"order": "desc"}}]
    }


def query_exists(field: str, size: int = 20) -> dict:
    return {
        "size": size,
        "query": {
            "bool": {
                "filter": [
                    {"term": {"nivelSigilo": 0}},
                    {"exists": {"field": field}}
                ]
            }
        },
        "sort": [{"@timestamp": {"order": "desc"}}]
    }


def query_grau(grau: str, size: int = 20) -> dict:
    return {
        "size": size,
        "query": {
            "bool": {
                "filter": [
                    {"term": {"nivelSigilo": 0}},
                    {"term": {"grau": grau}}
                ]
            }
        },
        "sort": [{"@timestamp": {"order": "desc"}}]
    }


def query_grau_exists(grau: str, field: str, size: int = 20) -> dict:
    return {
        "size": size,
        "query": {
            "bool": {
                "filter": [
                    {"term": {"nivelSigilo": 0}},
                    {"term": {"grau": grau}},
                    {"exists": {"field": field}}
                ]
            }
        },
        "sort": [{"@timestamp": {"order": "desc"}}]
    }