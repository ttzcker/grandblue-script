#这个reload(page)指令是模拟手点gbf里面Reload这个按键
def reload(page):
    page.evaluate("""
    () => {
        const btn = document.querySelector('.btn-treasure-footer-reload');

        if (btn) {
            const rect = btn.getBoundingClientRect();
            const x = rect.left + rect.width / 2;
            const y = rect.top + rect.height / 2;

            btn.dispatchEvent(new MouseEvent('mousedown', {
                bubbles: true,
                clientX: x,
                clientY: y
            }));

            btn.dispatchEvent(new MouseEvent('mouseup', {
                bubbles: true,
                clientX: x,
                clientY: y
            }));

            btn.dispatchEvent(new MouseEvent('click', {
                bubbles: true,
                clientX: x,
                clientY: y
            }));
        }
    }
    """)
