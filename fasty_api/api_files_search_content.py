import fasty
from fastapi import Request, Depends, Body, Response
import fasty.JWT
import fasty.JWT_Docs
import api_models.documents as Docs
from ReCompact.db_async import get_db_context
import api_models.documents as Docs
import ReCompact.es_search as search_engine


def search_content_of_file(app_name: str, content: str):
    """
    Thực hiện tìm kiếm ter6n nội dung của file
    :param app_name: app
    :param content: nội dung
    :return:
    """
    str_content = content
    highlight = {
        "pre_tags": ["<em>"],
        "post_tags": ["</em>"],
        "fields": {
            "content": {}
        }
    }
    match_phraseBody = {
        "match_phrase": {
            "content": {
                "query": str_content,
                "slop": 3,
                "analyzer": "standard",
                "zero_terms_query": "none",
                "boost": 4.5
            }
        }
    }
    search_body_2 = {
        "match": {
            "content": {
                "query": str_content,
                "boost": 0.5

            }
        }
    }
    search_body = {
        "multi_match": {
            "query": str_content,
            "fields": ["content"],
            "type": "phrase"
        }
    }
    should_body = {
        "bool": {
            "should": [
                match_phraseBody,
                search_body_2,
                search_body

            ]
        }
    }
    prefix_app = {
        "prefix": {
            "path.virtual": f'/{app_name}/'
        }
    }
    bool_body = {
        "bool": {
            "must": [
                prefix_app,
                should_body
            ]

        }
    }
    resp = search_engine.get_client().search(index=fasty.config.search.index, query=bool_body, highlight=highlight)
    total_items = resp['hits']['total']['value']
    max_score = resp["hits"].get('max_score')
    ret_list = []
    for hit in resp['hits']['hits']:
        highlight_contents = hit["highlight"].get('content', [])
        res_content = hit["_source"].get('content')
        score = hit.get("score")
        file_name = hit["_source"]["file"]["filename"]
        ret_list.append(dict(
            highlight=highlight_contents,
            content=res_content,
            score=score,
            server_file_id=file_name  # Tên file
        ))
    return dict(
        total_items=total_items,
        max_score=max_score,
        items=ret_list,
        text_search=content
    )


@fasty.api_post("/{app_name}/search")
async def file_search(app_name: str, content: str = Body(embed=True), token: str = Depends(fasty.JWT.oauth2_scheme)):
    db_name = await fasty.JWT.get_db_name_async(app_name)
    if db_name is None:
        return Response(status_code=403)
    search_result = search_content_of_file(app_name, content)

    db_context = get_db_context(db_name)
    ret_items = []
    url = fasty.config.app.api_url
    for x in search_result["items"]:
        upload_id = x["server_file_id"].split('.')[0]  # tách lấy id upload
        upload_doc_item = await db_context.find_one_async(
            Docs.Files,
            Docs.Files._id == upload_id
        )  # upload_docs.find_one(upload_docs._id == upload_id)

        if upload_doc_item:
            upload_doc_item['Highlight'] = x.get('highlight', [])
            upload_doc_item[
                "UrlOfServerPath"] = url + f"/{app_name}/file/{upload_doc_item[Docs.Files.FullFileName.__name__]}"
            upload_doc_item["AppName"] = app_name
            upload_doc_item[
                "RelUrlOfServerPath"] = f"/{app_name}/file/{upload_doc_item[Docs.Files.FullFileName.__name__]}"
            upload_doc_item[
                "ThumbUrl"] = url + f"/{app_name}/thumb/{upload_doc_item['_id']}/{upload_doc_item[Docs.Files.FileName.__name__]}.png"
            ret_items += [upload_doc_item]

    return dict(
        total_items=search_result["total_items"],
        max_score=search_result["max_score"],
        items=ret_items,
        text_search=search_result["text_search"]
    )
