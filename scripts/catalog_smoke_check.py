from app import create_app
from app.services.catalog import TOOL_CATEGORIES


ENDPOINT_PATHS = {
    "pdf.merge": "/pdf/merge",
    "pdf.split": "/pdf/split",
    "pdf.compress": "/pdf/compress",
    "pdf.to_jpg": "/pdf/to-jpg",
    "image.compress": "/image/compress",
    "image.resize": "/image/resize",
    "image.convert": "/image/convert",
    "text.word_counter": "/text/word-counter",
    "text.case_converter": "/text/case-converter",
    "dev.json_formatter": "/dev/json-formatter",
    "dev.base64_tool": "/dev/base64",
    "dev.uuid_generator": "/dev/uuid",
    "calc.emi": "/calculators/emi",
    "calc.age": "/calculators/age",
}


def main():
    app = create_app()
    client = app.test_client()
    failures = []

    dashboard = client.get("/")
    dashboard_html = dashboard.get_data(as_text=True)
    if dashboard.status_code != 200:
        failures.append(("/", "GET", dashboard.status_code, "dashboard did not render"))
    if "{{ current_year }}" in dashboard_html:
        failures.append(("/", "GET", 200, "current_year was not rendered"))
    if "Utility Tools Hub" not in dashboard_html:
        failures.append(("/", "GET", 200, "base layout did not render expected brand"))

    for category in TOOL_CATEGORIES:
        for tool in category["tools"]:
            if "endpoint" in tool:
                path = ENDPOINT_PATHS.get(tool["endpoint"])
                if not path:
                    failures.append((tool["name"], "CONFIG", "missing", tool["endpoint"]))
                    continue
                response = client.get(path)
                if response.status_code != 200:
                    failures.append((path, "GET", response.status_code, tool["name"]))
                continue

            path = f"/tools/{tool['slug']}"
            get_response = client.get(path)
            if get_response.status_code != 200:
                failures.append((path, "GET", get_response.status_code, tool["name"]))

            post_response = client.post(path)
            post_html = post_response.get_data(as_text=True)
            if post_response.status_code != 200:
                failures.append((path, "POST", post_response.status_code, tool["name"]))
            elif tool.get("kind") == "planned" and "Next step:" not in post_html:
                failures.append((path, "POST", 200, "setup plan missing"))

    if failures:
        print("Catalog smoke check failed:")
        for failure in failures:
            print(failure)
        raise SystemExit(1)

    print("Catalog smoke check passed.")


if __name__ == "__main__":
    main()
