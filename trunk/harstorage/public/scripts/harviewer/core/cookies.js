require.def("core/cookies",["core/lib"],function(a){var b={getCookie:function(b){var c=document.cookie.split(";");for(var d=0;d<c.length;d++){var e=c[d].split("=");if(a.trim(e[0])==b)return e[1].length?unescape(a.trim(e[1])):null}},setCookie:function(a,b,c,d,e,f){var g=new Date;g.setTime(g.getTime()),c&&(c=c*1e3*60*60*24);var h=new Date(g.getTime()+c);document.cookie=a+"="+escape(b)+(c?";expires="+h.toGMTString():"")+(d?";path="+d:"")+(e?";domain="+e:"")+(f?";secure":"")},removeCookie:function(a,b,c){this.getCookie(a)&&(document.cookie=a+"="+(b?";path="+b:"")+(c?";domain="+c:"")+";expires=Thu, 01-Jan-1970 00:00:01 GMT")}};return b})