# Cây form duy nhất — API01 và Screen01

```text
architecture/
├── apps/
│   ├── server/
│   │   ├── README.md
│   │   ├── app/
│   │   │   ├── main.md                          # main.py: bootstrap
│   │   │   ├── api/v1.md                        # api/v1.py: route registration
│   │   │   ├── core/
│   │   │   │   ├── config.md                    # config.py: validated settings
│   │   │   │   ├── database.md                  # database.py: sessions
│   │   │   │   └── security/access_token.md     # access_token.py: identity
│   │   │   ├── modules/module1/api01/
│   │   │   │   ├── README.md                    # Tổng quan API duy nhất
│   │   │   │   ├── __init__.md                  # __init__.py
│   │   │   │   ├── models.md                    # models.py
│   │   │   │   ├── validate.md                  # validate.py
│   │   │   │   ├── query.md                     # query.py
│   │   │   │   └── view.md                      # view.py
│   │   │   ├── service/provider.md             # provider.py: external adapter
│   │   │   └── utils/auth.md                    # auth.py: policy
│   │   ├── tests/test_api01.md                 # test_api01.py
│   │   └── docs/dd/module1/api01/README.md    # DD cho chính API01
│   └── client/
│       ├── src/
│       │   ├── main.ts.md                      # main.ts: UI bootstrap
│       │   └── app/
│       │       ├── app.routes.ts.md            # App routes
│       │       ├── core/http/api-client.service.ts.md
│       │       ├── features/module1/screen01/
│       │       │   ├── README.md               # Tổng quan screen duy nhất
│       │       │   ├── pages/
│       │       │   │   ├── screen01-page.ts.md
│       │       │   │   ├── screen01-page.html.md
│       │       │   │   └── screen01-page.css.md
│       │       │   ├── data-access/screen01.service.ts.md
│       │       │   ├── models/screen01.model.ts.md
│       │       │   ├── ui/screen01-widget.ts.md
│       │       │   └── screen01.spec.ts.md
│       │       ├── layouts/main-layout.ts.md
│       │       └── shared/ui/button.ts.md
│       └── docs/dd_screens/screen01/README.md # DD cho chính Screen01
├── PROJECT.md                                # Chưa cấu hình repo đích
├── TEMPLATE_CONFIG.json                      # Các mẫu chỉ tham khảo
└── EXAMPLE_MAP.json                          # 1:1 source-form → Markdown
```

**Mỗi thư mục trong cây trên đều có README.md** (không lặp ở sơ đồ). Không có nguồn `.py`, `.ts` hay ảnh thực trong bộ kit; những tên đó biểu thị **vị trí tài liệu mô tả code**, không phải bản sao code.
