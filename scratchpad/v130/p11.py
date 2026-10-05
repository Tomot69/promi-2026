import io
W=io.open('Promi+Design.swift',encoding='utf-8').read()
old="""            s == .dark ? Color(red: 0.2000, green: 0.3255, blue: 0.5098) : Color(red: 0.8118, green: 0.8980, blue: 0.9961)"""
assert W.count(old)==1; W=W.replace(old,"""            s == .dark ? Color(red: 0.5412, green: 0.7961, blue: 0.9098) : Color(red: 0.8118, green: 0.8980, blue: 0.9961)""")
old="""        static let bleu35 = Color(red: 0.2000, green: 0.3255, blue: 0.5098)   // #335382"""
assert W.count(old)==1; W=W.replace(old, old+"""\n        static let tropical78 = Color(red: 0.5412, green: 0.7961, blue: 0.9098)   // #8ACBE8""")
io.open('Promi+Design.swift','w',encoding='utf-8').write(W)
