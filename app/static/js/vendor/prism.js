"use strict";

/* http://prismjs.com/download.html?themes=prism&languages=markup+css+clike+javascript+python+jsx+scss&plugins=show-language+normalize-whitespace */
var _self = "undefined" != typeof window ? window : "undefined" != typeof WorkerGlobalScope && self instanceof WorkerGlobalScope ? self : {},
    Prism = function () {
  var e = /\blang(?:uage)?-(\w+)\b/i,
      t = 0,
      n = _self.Prism = { util: { encode: function encode(e) {
        return e instanceof a ? new a(e.type, n.util.encode(e.content), e.alias) : "Array" === n.util.type(e) ? e.map(n.util.encode) : e.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/\u00a0/g, " ");
      }, type: function type(e) {
        return Object.prototype.toString.call(e).match(/\[object (\w+)\]/)[1];
      }, objId: function objId(e) {
        return e.__id || Object.defineProperty(e, "__id", { value: ++t }), e.__id;
      }, clone: function clone(e) {
        var t = n.util.type(e);switch (t) {case "Object":
            var a = {};for (var r in e) {
              e.hasOwnProperty(r) && (a[r] = n.util.clone(e[r]));
            }return a;case "Array":
            return e.map && e.map(function (e) {
              return n.util.clone(e);
            });}return e;
      } }, languages: { extend: function extend(e, t) {
        var a = n.util.clone(n.languages[e]);for (var r in t) {
          a[r] = t[r];
        }return a;
      }, insertBefore: function insertBefore(e, t, a, r) {
        r = r || n.languages;var l = r[e];if (2 == arguments.length) {
          a = arguments[1];for (var i in a) {
            a.hasOwnProperty(i) && (l[i] = a[i]);
          }return l;
        }var o = {};for (var s in l) {
          if (l.hasOwnProperty(s)) {
            if (s == t) for (var i in a) {
              a.hasOwnProperty(i) && (o[i] = a[i]);
            }o[s] = l[s];
          }
        }return n.languages.DFS(n.languages, function (t, n) {
          n === r[e] && t != e && (this[t] = o);
        }), r[e] = o;
      }, DFS: function DFS(e, t, a, r) {
        r = r || {};for (var l in e) {
          e.hasOwnProperty(l) && (t.call(e, l, e[l], a || l), "Object" !== n.util.type(e[l]) || r[n.util.objId(e[l])] ? "Array" !== n.util.type(e[l]) || r[n.util.objId(e[l])] || (r[n.util.objId(e[l])] = !0, n.languages.DFS(e[l], t, l, r)) : (r[n.util.objId(e[l])] = !0, n.languages.DFS(e[l], t, null, r)));
        }
      } }, plugins: {}, highlightAll: function highlightAll(e, t) {
      var a = { callback: t, selector: 'code[class*="language-"], [class*="language-"] code, code[class*="lang-"], [class*="lang-"] code' };n.hooks.run("before-highlightall", a);for (var r, l = a.elements || document.querySelectorAll(a.selector), i = 0; r = l[i++];) {
        n.highlightElement(r, e === !0, a.callback);
      }
    }, highlightElement: function highlightElement(t, a, r) {
      for (var l, i, o = t; o && !e.test(o.className);) {
        o = o.parentNode;
      }o && (l = (o.className.match(e) || [, ""])[1], i = n.languages[l]), t.className = t.className.replace(e, "").replace(/\s+/g, " ") + " language-" + l, o = t.parentNode, /pre/i.test(o.nodeName) && (o.className = o.className.replace(e, "").replace(/\s+/g, " ") + " language-" + l);var s = t.textContent,
          u = { element: t, language: l, grammar: i, code: s };if (!s || !i) return n.hooks.run("complete", u), void 0;if (n.hooks.run("before-highlight", u), a && _self.Worker) {
        var c = new Worker(n.filename);c.onmessage = function (e) {
          u.highlightedCode = e.data, n.hooks.run("before-insert", u), u.element.innerHTML = u.highlightedCode, r && r.call(u.element), n.hooks.run("after-highlight", u), n.hooks.run("complete", u);
        }, c.postMessage(JSON.stringify({ language: u.language, code: u.code, immediateClose: !0 }));
      } else u.highlightedCode = n.highlight(u.code, u.grammar, u.language), n.hooks.run("before-insert", u), u.element.innerHTML = u.highlightedCode, r && r.call(t), n.hooks.run("after-highlight", u), n.hooks.run("complete", u);
    }, highlight: function highlight(e, t, r) {
      var l = n.tokenize(e, t);return a.stringify(n.util.encode(l), r);
    }, tokenize: function tokenize(e, t) {
      var a = n.Token,
          r = [e],
          l = t.rest;if (l) {
        for (var i in l) {
          t[i] = l[i];
        }delete t.rest;
      }e: for (var i in t) {
        if (t.hasOwnProperty(i) && t[i]) {
          var o = t[i];o = "Array" === n.util.type(o) ? o : [o];for (var s = 0; s < o.length; ++s) {
            var u = o[s],
                c = u.inside,
                g = !!u.lookbehind,
                h = !!u.greedy,
                f = 0,
                d = u.alias;u = u.pattern || u;for (var p = 0; p < r.length; p++) {
              var m = r[p];if (r.length > e.length) break e;if (!(m instanceof a)) {
                u.lastIndex = 0;var v = u.exec(m),
                    y = 1;if (!v && h && p != r.length - 1) {
                  var b = r[p + 1].matchedStr || r[p + 1],
                      k = m + b;if (p < r.length - 2 && (k += r[p + 2].matchedStr || r[p + 2]), u.lastIndex = 0, v = u.exec(k), !v) continue;var w = v.index + (g ? v[1].length : 0);if (w >= m.length) continue;var _ = v.index + v[0].length,
                      P = m.length + b.length;y = 3, P >= _ && (y = 2, k = k.slice(0, P)), m = k;
                }if (v) {
                  g && (f = v[1].length);var w = v.index + f,
                      v = v[0].slice(f),
                      _ = w + v.length,
                      S = m.slice(0, w),
                      O = m.slice(_),
                      j = [p, y];S && j.push(S);var A = new a(i, c ? n.tokenize(v, c) : v, d, v);j.push(A), O && j.push(O), Array.prototype.splice.apply(r, j);
                }
              }
            }
          }
        }
      }return r;
    }, hooks: { all: {}, add: function add(e, t) {
        var a = n.hooks.all;a[e] = a[e] || [], a[e].push(t);
      }, run: function run(e, t) {
        var a = n.hooks.all[e];if (a && a.length) for (var r, l = 0; r = a[l++];) {
          r(t);
        }
      } } },
      a = n.Token = function (e, t, n, a) {
    this.type = e, this.content = t, this.alias = n, this.matchedStr = a || null;
  };if (a.stringify = function (e, t, r) {
    if ("string" == typeof e) return e;if ("Array" === n.util.type(e)) return e.map(function (n) {
      return a.stringify(n, t, e);
    }).join("");var l = { type: e.type, content: a.stringify(e.content, t, r), tag: "span", classes: ["token", e.type], attributes: {}, language: t, parent: r };if ("comment" == l.type && (l.attributes.spellcheck = "true"), e.alias) {
      var i = "Array" === n.util.type(e.alias) ? e.alias : [e.alias];Array.prototype.push.apply(l.classes, i);
    }n.hooks.run("wrap", l);var o = "";for (var s in l.attributes) {
      o += (o ? " " : "") + s + '="' + (l.attributes[s] || "") + '"';
    }return "<" + l.tag + ' class="' + l.classes.join(" ") + '" ' + o + ">" + l.content + "</" + l.tag + ">";
  }, !_self.document) return _self.addEventListener ? (_self.addEventListener("message", function (e) {
    var t = JSON.parse(e.data),
        a = t.language,
        r = t.code,
        l = t.immediateClose;_self.postMessage(n.highlight(r, n.languages[a], a)), l && _self.close();
  }, !1), _self.Prism) : _self.Prism;var r = document.currentScript || [].slice.call(document.getElementsByTagName("script")).pop();return r && (n.filename = r.src, document.addEventListener && !r.hasAttribute("data-manual") && document.addEventListener("DOMContentLoaded", n.highlightAll)), _self.Prism;
}();"undefined" != typeof module && module.exports && (module.exports = Prism), "undefined" != typeof global && (global.Prism = Prism);
Prism.languages.markup = { comment: /<!--[\w\W]*?-->/, prolog: /<\?[\w\W]+?\?>/, doctype: /<!DOCTYPE[\w\W]+?>/, cdata: /<!\[CDATA\[[\w\W]*?]]>/i, tag: { pattern: /<\/?(?!\d)[^\s>\/=.$<]+(?:\s+[^\s>\/=]+(?:=(?:("|')(?:\\\1|\\?(?!\1)[\w\W])*\1|[^\s'">=]+))?)*\s*\/?>/i, inside: { tag: { pattern: /^<\/?[^\s>\/]+/i, inside: { punctuation: /^<\/?/, namespace: /^[^\s>\/:]+:/ } }, "attr-value": { pattern: /=(?:('|")[\w\W]*?(\1)|[^\s>]+)/i, inside: { punctuation: /[=>"']/ } }, punctuation: /\/?>/, "attr-name": { pattern: /[^\s>\/]+/, inside: { namespace: /^[^\s>\/:]+:/ } } } }, entity: /&#?[\da-z]{1,8};/i }, Prism.hooks.add("wrap", function (a) {
  "entity" === a.type && (a.attributes.title = a.content.replace(/&amp;/, "&"));
}), Prism.languages.xml = Prism.languages.markup, Prism.languages.html = Prism.languages.markup, Prism.languages.mathml = Prism.languages.markup, Prism.languages.svg = Prism.languages.markup;
Prism.languages.css = { comment: /\/\*[\w\W]*?\*\//, atrule: { pattern: /@[\w-]+?.*?(;|(?=\s*\{))/i, inside: { rule: /@[\w-]+/ } }, url: /url\((?:(["'])(\\(?:\r\n|[\w\W])|(?!\1)[^\\\r\n])*\1|.*?)\)/i, selector: /[^\{\}\s][^\{\};]*?(?=\s*\{)/, string: /("|')(\\(?:\r\n|[\w\W])|(?!\1)[^\\\r\n])*\1/, property: /(\b|\B)[\w-]+(?=\s*:)/i, important: /\B!important\b/i, "function": /[-a-z0-9]+(?=\()/i, punctuation: /[(){};:]/ }, Prism.languages.css.atrule.inside.rest = Prism.util.clone(Prism.languages.css), Prism.languages.markup && (Prism.languages.insertBefore("markup", "tag", { style: { pattern: /(<style[\w\W]*?>)[\w\W]*?(?=<\/style>)/i, lookbehind: !0, inside: Prism.languages.css, alias: "language-css" } }), Prism.languages.insertBefore("inside", "attr-value", { "style-attr": { pattern: /\s*style=("|').*?\1/i, inside: { "attr-name": { pattern: /^\s*style/i, inside: Prism.languages.markup.tag.inside }, punctuation: /^\s*=\s*['"]|['"]\s*$/, "attr-value": { pattern: /.+/i, inside: Prism.languages.css } }, alias: "language-css" } }, Prism.languages.markup.tag));
Prism.languages.clike = { comment: [{ pattern: /(^|[^\\])\/\*[\w\W]*?\*\//, lookbehind: !0 }, { pattern: /(^|[^\\:])\/\/.*/, lookbehind: !0 }], string: { pattern: /(["'])(\\(?:\r\n|[\s\S])|(?!\1)[^\\\r\n])*\1/, greedy: !0 }, "class-name": { pattern: /((?:\b(?:class|interface|extends|implements|trait|instanceof|new)\s+)|(?:catch\s+\())[a-z0-9_\.\\]+/i, lookbehind: !0, inside: { punctuation: /(\.|\\)/ } }, keyword: /\b(if|else|while|do|for|return|in|instanceof|function|new|try|throw|catch|finally|null|break|continue)\b/, "boolean": /\b(true|false)\b/, "function": /[a-z0-9_]+(?=\()/i, number: /\b-?(?:0x[\da-f]+|\d*\.?\d+(?:e[+-]?\d+)?)\b/i, operator: /--?|\+\+?|!=?=?|<=?|>=?|==?=?|&&?|\|\|?|\?|\*|\/|~|\^|%/, punctuation: /[{}[\];(),.:]/ };
Prism.languages.javascript = Prism.languages.extend("clike", { keyword: /\b(as|async|await|break|case|catch|class|const|continue|debugger|default|delete|do|else|enum|export|extends|finally|for|from|function|get|if|implements|import|in|instanceof|interface|let|new|null|of|package|private|protected|public|return|set|static|super|switch|this|throw|try|typeof|var|void|while|with|yield)\b/, number: /\b-?(0x[\dA-Fa-f]+|0b[01]+|0o[0-7]+|\d*\.?\d+([Ee][+-]?\d+)?|NaN|Infinity)\b/, "function": /[_$a-zA-Z\xA0-\uFFFF][_$a-zA-Z0-9\xA0-\uFFFF]*(?=\()/i }), Prism.languages.insertBefore("javascript", "keyword", { regex: { pattern: /(^|[^\/])\/(?!\/)(\[.+?]|\\.|[^\/\\\r\n])+\/[gimyu]{0,5}(?=\s*($|[\r\n,.;})]))/, lookbehind: !0, greedy: !0 } }), Prism.languages.insertBefore("javascript", "class-name", { "template-string": { pattern: /`(?:\\\\|\\?[^\\])*?`/, inside: { interpolation: { pattern: /\$\{[^}]+\}/, inside: { "interpolation-punctuation": { pattern: /^\$\{|\}$/, alias: "punctuation" }, rest: Prism.languages.javascript } }, string: /[\s\S]+/ } } }), Prism.languages.markup && Prism.languages.insertBefore("markup", "tag", { script: { pattern: /(<script[\w\W]*?>)[\w\W]*?(?=<\/script>)/i, lookbehind: !0, inside: Prism.languages.javascript, alias: "language-javascript" } }), Prism.languages.js = Prism.languages.javascript;
Prism.languages.python = { "triple-quoted-string": { pattern: /"""[\s\S]+?"""|'''[\s\S]+?'''/, alias: "string" }, comment: { pattern: /(^|[^\\])#.*/, lookbehind: !0 }, string: /("|')(?:\\?.)*?\1/, "function": { pattern: /((?:^|\s)def[ \t]+)[a-zA-Z_][a-zA-Z0-9_]*(?=\()/g, lookbehind: !0 }, "class-name": { pattern: /(\bclass\s+)[a-z0-9_]+/i, lookbehind: !0 }, keyword: /\b(?:as|assert|async|await|break|class|continue|def|del|elif|else|except|exec|finally|for|from|global|if|import|in|is|lambda|pass|print|raise|return|try|while|with|yield)\b/, "boolean": /\b(?:True|False)\b/, number: /\b-?(?:0[bo])?(?:(?:\d|0x[\da-f])[\da-f]*\.?\d*|\.\d+)(?:e[+-]?\d+)?j?\b/i, operator: /[-+%=]=?|!=|\*\*?=?|\/\/?=?|<[<=>]?|>[=>]?|[&|^~]|\b(?:or|and|not)\b/, punctuation: /[{}[\];(),.:]/ };
!function (a) {
  var e = a.util.clone(a.languages.javascript);a.languages.jsx = a.languages.extend("markup", e), a.languages.jsx.tag.pattern = /<\/?[\w\.:-]+\s*(?:\s+[\w\.:-]+(?:=(?:("|')(\\?[\w\W])*?\1|[^\s'">=]+|(\{[\w\W]*?\})))?\s*)*\/?>/i, a.languages.jsx.tag.inside["attr-value"].pattern = /=[^\{](?:('|")[\w\W]*?(\1)|[^\s>]+)/i;var s = a.util.clone(a.languages.jsx);delete s.punctuation, s = a.languages.insertBefore("jsx", "operator", { punctuation: /=(?={)|[{}[\];(),.:]/ }, { jsx: s }), a.languages.insertBefore("inside", "attr-value", { script: { pattern: /=(\{(?:\{[^}]*\}|[^}])+\})/i, inside: s, alias: "language-javascript" } }, a.languages.jsx.tag);
}(Prism);
Prism.languages.scss = Prism.languages.extend("css", { comment: { pattern: /(^|[^\\])(?:\/\*[\w\W]*?\*\/|\/\/.*)/, lookbehind: !0 }, atrule: { pattern: /@[\w-]+(?:\([^()]+\)|[^(])*?(?=\s+[{;])/, inside: { rule: /@[\w-]+/ } }, url: /(?:[-a-z]+-)*url(?=\()/i, selector: { pattern: /(?=\S)[^@;\{\}\(\)]?([^@;\{\}\(\)]|&|#\{\$[-_\w]+\})+(?=\s*\{(\}|\s|[^\}]+(:|\{)[^\}]+))/m, inside: { placeholder: /%[-_\w]+/ } } }), Prism.languages.insertBefore("scss", "atrule", { keyword: [/@(?:if|else(?: if)?|for|each|while|import|extend|debug|warn|mixin|include|function|return|content)/i, { pattern: /( +)(?:from|through)(?= )/, lookbehind: !0 }] }), Prism.languages.insertBefore("scss", "property", { variable: /\$[-_\w]+|#\{\$[-_\w]+\}/ }), Prism.languages.insertBefore("scss", "function", { placeholder: { pattern: /%[-_\w]+/, alias: "selector" }, statement: /\B!(?:default|optional)\b/i, "boolean": /\b(?:true|false)\b/, "null": /\bnull\b/, operator: { pattern: /(\s)(?:[-+*\/%]|[=!]=|<=?|>=?|and|or|not)(?=\s)/, lookbehind: !0 } }), Prism.languages.scss.atrule.inside.rest = Prism.util.clone(Prism.languages.scss);
!function () {
  if ("undefined" != typeof self && self.Prism && self.document) {
    var e = { html: "HTML", xml: "XML", svg: "SVG", mathml: "MathML", css: "CSS", clike: "C-like", javascript: "JavaScript", abap: "ABAP", actionscript: "ActionScript", apacheconf: "Apache Configuration", apl: "APL", applescript: "AppleScript", asciidoc: "AsciiDoc", aspnet: "ASP.NET (C#)", autoit: "AutoIt", autohotkey: "AutoHotkey", basic: "BASIC", csharp: "C#", cpp: "C++", coffeescript: "CoffeeScript", "css-extras": "CSS Extras", fsharp: "F#", glsl: "GLSL", http: "HTTP", inform7: "Inform 7", json: "JSON", latex: "LaTeX", lolcode: "LOLCODE", matlab: "MATLAB", mel: "MEL", nasm: "NASM", nginx: "nginx", nsis: "NSIS", objectivec: "Objective-C", ocaml: "OCaml", parigp: "PARI/GP", php: "PHP", "php-extras": "PHP Extras", powershell: "PowerShell", jsx: "React JSX", rest: "reST (reStructuredText)", sas: "SAS", sass: "Sass (Sass)", scss: "Sass (Scss)", sql: "SQL", typescript: "TypeScript", vhdl: "VHDL", vim: "vim", wiki: "Wiki markup", yaml: "YAML" };Prism.hooks.add("before-highlight", function (s) {
      var a = s.element.parentNode;if (a && /pre/i.test(a.nodeName)) {
        var t,
            i,
            r = a.getAttribute("data-language") || e[s.language] || s.language.substring(0, 1).toUpperCase() + s.language.substring(1),
            l = a.previousSibling;l && /\s*\bprism-show-language\b\s*/.test(l.className) && l.firstChild && /\s*\bprism-show-language-label\b\s*/.test(l.firstChild.className) ? i = l.firstChild : (t = document.createElement("div"), i = document.createElement("div"), i.className = "prism-show-language-label", t.className = "prism-show-language", t.appendChild(i), a.parentNode.insertBefore(t, a)), i.innerHTML = r;
      }
    });
  }
}();
!function () {
  function e(e) {
    this.defaults = r({}, e);
  }function n(e) {
    return e.replace(/-(\w)/g, function (e, n) {
      return n.toUpperCase();
    });
  }function t(e) {
    for (var n = 0, t = 0; t < e.length; ++t) {
      e.charCodeAt(t) == "	".charCodeAt(0) && (n += 3);
    }return e.length + n;
  }if ("undefined" != typeof self && self.Prism && self.document) {
    var r = Object.assign || function (e, n) {
      for (var t in n) {
        n.hasOwnProperty(t) && (e[t] = n[t]);
      }return e;
    };e.prototype = { setDefaults: function setDefaults(e) {
        this.defaults = r(this.defaults, e);
      }, normalize: function normalize(e, t) {
        t = r(this.defaults, t);for (var i in t) {
          var o = n(i);"normalize" !== i && "setDefaults" !== o && t[i] && this[o] && (e = this[o].call(this, e, t[i]));
        }return e;
      }, leftTrim: function leftTrim(e) {
        return e.replace(/^\s+/, "");
      }, rightTrim: function rightTrim(e) {
        return e.replace(/\s+$/, "");
      }, tabsToSpaces: function tabsToSpaces(e, n) {
        return n = 0 | n || 4, e.replace(/\t/g, new Array(++n).join(" "));
      }, spacesToTabs: function spacesToTabs(e, n) {
        return n = 0 | n || 4, e.replace(new RegExp(" {" + n + "}", "g"), "	");
      }, removeTrailing: function removeTrailing(e) {
        return e.replace(/\s*?$/gm, "");
      }, removeInitialLineFeed: function removeInitialLineFeed(e) {
        return e.replace(/^(?:\r?\n|\r)/, "");
      }, removeIndent: function removeIndent(e) {
        var n = e.match(/^[^\S\n\r]*(?=\S)/gm);return n && n[0].length ? (n.sort(function (e, n) {
          return e.length - n.length;
        }), n[0].length ? e.replace(new RegExp("^" + n[0], "gm"), "") : e) : e;
      }, indent: function indent(e, n) {
        return e.replace(/^[^\S\n\r]*(?=\S)/gm, new Array(++n).join("	") + "$&");
      }, breakLines: function breakLines(e, n) {
        n = n === !0 ? 80 : 0 | n || 80;for (var r = e.split("\n"), i = 0; i < r.length; ++i) {
          if (!(t(r[i]) <= n)) {
            for (var o = r[i].split(/(\s+)/g), a = 0, l = 0; l < o.length; ++l) {
              var s = t(o[l]);a += s, a > n && (o[l] = "\n" + o[l], a = s);
            }r[i] = o.join("");
          }
        }return r.join("\n");
      } }, Prism.plugins.NormalizeWhitespace = new e({ "remove-trailing": !0, "remove-indent": !0, "left-trim": !0, "right-trim": !0 }), Prism.hooks.add("before-highlight", function (e) {
      var n = e.element.parentNode;if (e.code && n && "pre" === n.nodeName.toLowerCase() && (!e.settings || e.settings["whitespace-normalization"] !== !1)) {
        for (var t = n.childNodes, r = "", i = "", o = !1, a = Prism.plugins.NormalizeWhitespace, l = 0; l < t.length; ++l) {
          var s = t[l];s == e.element ? o = !0 : "#text" === s.nodeName && (o ? i += s.nodeValue : r += s.nodeValue, n.removeChild(s), --l);
        }if (e.element.children.length && Prism.plugins.KeepMarkup) {
          var u = r + e.element.innerHTML + i;e.element.innerHTML = a.normalize(u, e.settings), e.code = e.element.textContent;
        } else e.code = r + e.code + i, e.code = a.normalize(e.code, e.settings);
      }
    });var i = Prism.hooks.all["before-highlight"];i.unshift(i.pop());
  }
}();