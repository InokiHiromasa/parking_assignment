import xml.dom.minidom


class XMLParser(object):

    def _check_file_name(self, file, type = ""):
        if isinstance(file, basestring):
            if not file.endswith('%s.xml' %type):
                file = file + type + '.xml'
        elif is_pathlib_path(file):
            if not file.name.endswith('%s.xml' %type):
                file = file.parent / (file.name + type + '.xml')
        return file

    def get_edges(self, file):
        fid = self._check_file_name(file, ".net")
        edges = []
        dom = xml.dom.minidom.parse(fid)
        for edge in dom.getElementsByTagName("edge"):
            if edge.getAttribute("id")[0] != ":":
                edges.append(edge.getAttribute("id"))
        return edges

    def get_routes(self, file):
        fid = self._check_file_name(file, ".rou")
        veh = {}
        dom = xml.dom.minidom.parse(fid)
        v = dom.getElementsByTagName("vehicle")
        for e in v:
            id = e.getAttribute("id")
            veh[id] = {}
            veh[id]["depart"] = e.getAttribute("depart")
            veh[id]["route"] = e.childNodes[1].getAttribute("edges").split(" ")
        return veh


if __name__ == "__main__":
    pass
