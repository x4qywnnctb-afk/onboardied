import streamlit.components.v1 as components

def inject_clarity():
    # Zmodyfikowany kod dla ID: vipt8ozvdk
    # Używamy window.parent, aby wyjść z iframe Streamlit
    clarity_js = """
    <script type="text/javascript">
        (function(c,l,a,r,i,t,y){
            c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
            t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
            y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
        })(window.parent, window.parent.document, "clarity", "script", "vipt8ozvdk");
    </script>
    """
    components.html(clarity_js, height=0, width=0)
