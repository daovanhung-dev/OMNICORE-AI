"""Kiểm tra trình duyệt trên bản chạy cục bộ do người gọi khởi động."""
import argparse
from playwright.sync_api import sync_playwright, expect

def check(url: str, chromium: str | None = None) -> None:
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path=chromium,headless=True,args=['--no-sandbox'])
        page=browser.new_page(viewport={'width':360,'height':740})
        page.goto(url+'/items');expect(page.get_by_role('heading',name='Danh mục')).to_be_visible()
        expect(page.get_by_text('Mục thứ nhất')).to_be_visible()
        expect(page.get_by_role('button',name='Trước')).to_be_disabled()
        page.get_by_role('button',name='Tiếp').click();expect(page.get_by_text('Mục thứ hai')).to_be_visible()
        expect(page.get_by_role('button',name='Tiếp')).to_be_disabled()
        page.get_by_role('button',name='Trước').click();expect(page.get_by_text('Mục thứ nhất')).to_be_visible()
        page.route('**/api/v1/items?*',lambda route:route.fulfill(status=503,body='{}'))
        page.get_by_role('button',name='Tải lại').click();expect(page.get_by_text('Không tải được dữ liệu. Hãy thử lại.')).to_be_visible()
        page.unroute('**/api/v1/items?*');page.get_by_role('button',name='Tải lại').click();expect(page.get_by_text('Mục thứ nhất')).to_be_visible()
        page.route('**/api/v1/items?*',lambda route:route.fulfill(json={'data':{'items':[],'total':0,'page':1,'page_size':1}}))
        page.get_by_role('button',name='Tải lại').click();expect(page.get_by_text('Không có dữ liệu')).to_be_visible()
        page.unroute('**/api/v1/items?*');page.goto(url+'/');expect(page.get_by_text('Mục thứ nhất')).to_be_visible()
        page.goto(url+'/items');expect(page.get_by_text('Mục thứ nhất')).to_be_visible()
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        browser.close()
    print('ĐẠT: tuyến gốc/trực tiếp, dữ liệu thật, phân trang, lỗi mô phỏng, tải lại, rỗng mô phỏng, bố cục 360px')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--url',default='http://127.0.0.1:8766');p.add_argument('--chromium');a=p.parse_args();check(a.url,a.chromium)
