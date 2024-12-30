//window.onload指定加载完网页后再执行代码，因为引用js文件的html是顺序执行文件，在head执行此js时数据未加载，可能导致报错
window.onload = function () {
    const {createEditor, createToolbar} = window.wangEditor

    const editorConfig = {
        placeholder: '在此输入...',
        onChange(editor) {
            const html = editor.getHtml()
            console.log('editor content', html)
            // 也可以同步到 <textarea>
        },
    }

    const editor = createEditor({
        selector: '#editor-container',
        html: '<p><br></p>',
        config: editorConfig,
        mode: 'default', // or 'simple'
    })

    const toolbarConfig = {}

    const toolbar = createToolbar({
        editor,
        selector: '#toolbar-container',
        config: toolbarConfig,
        mode: 'default', // or 'simple'
    })

    $("#submit-btn").click(function (event) {
            // 组织默认行为，防止走表单发送数据而非ajax
            event.preventDefault();
            let title = $("input[name='title']").val();
            let category = $("#category-select").val();
            let content = editor.getHtml();  // 相对的getText只返回文本，理解：getHtml会返回标签如<h1></h1>
            let csrfmiddlewaretoken = $("input[name='csrfmiddlewaretoken']").val();  //csrf...在网络源代码中form下的隐藏字段可以找到（网页端按F12）
            //ai补充:在 Django 中，当你在 HTML 表单中使用 {% csrf_token %} 模板标签时，Django 会自动生成一个隐藏的 input 标签，并且 name 属性值设置为 csrfmiddlewaretoken。这个隐藏的 input 标签包含了 CSRF 令牌
            $.ajax('/blog/pub', {
                method: 'POST',
                data: {title, category, content, csrfmiddlewaretoken},
                success: function (result) {
                    if (result['code'] == 200) {
                        // 获取博客id
                        let blog_id = result['data']['blog_id']
                        // 跳转到博客详情页面
                        window.location = '/blog/detail/' + blog_id
                    } else {
                        alert(result['message']);
                    }
                }
            })
        }
    )
}