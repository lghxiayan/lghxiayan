from lxml import etree

xml = """
<book>
    <id>1</id>
    <name>野花遍地香</name>
    <price>1.23</price>
    <nick>臭豆腐</nick>
    <author>
        <nick id='10086'>周大强</nick>
        <nick id='10010'>周芷若</nick>
        <nick class="joy">周杰伦</nick>
        <nick class="jolin">蔡依林</nick>
        <div>
            <nick>惹了</nick>
        </div>
        <div>文本</div>
        <div><span>文本</span></div>
    </author>

    <partner>
        <nick id='ppc'>胖胖陈</nick>
        <nick id='ppbc'>胖胖不陈</nick>
    </partner>
</book>

"""

tree = etree.XML(xml)
# result = tree.xpath('//author/div')[0].xpath("string()")
result = tree.xpath('//nick[contains(string(),"周")]/text()')
print(result)
