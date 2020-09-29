from ldmsd import ldmsd_request
from abc import ABC, abstractmethod, abstractclassmethod

# Make this an abstract class
class LDMSD_CFG_CMD(ABC):

    @abstractclassmethod
    def prdcr_add(cls, name, host, port, xprt, type, reconnect_interval):
        pass

    @abstractclassmethod
    def prdcr_start(cls, name):
        pass

    @abstractclassmethod
    def prdcr_stop(cls, name):
        pass

    @abstractclassmethod
    def prdcr_del(cls, name):
        pass

    @abstractclassmethod
    def updtr_add(cls, name, update_interval, update_offset,
                  push = None, perm = None, prdcrs = [], 
                  set_matches = {'set_name': [], 'schema': []}):
        pass

    @abstractclassmethod
    def updtr_del(cls, name):
        pass

    @abstractclassmethod
    def updtr_start(cls, name):
        pass

    @abstractclassmethod
    def updtr_stop(cls, name):
        pass

    @abstractclassmethod
    def strgp_add(cls, name, container, schema, plugin, prdcrs, metrics, perm):
        pass

    @abstractclassmethod
    def strgp_del(cls, name):
        pass

    @abstractclassmethod
    def strgp_start(cls, name):
        pass

    @abstractclassmethod
    def strgp_stop(cls, name):
        pass

class LDMSD_CFG_CMD_V4(LDMSD_CFG_CMD):

    @classmethod
    def prdcr_add(cls, name, host, port, xprt, type, reconnect_interval):
        return "prdcr_add name={name} host={host} xprt={xprt} type={type} " \
               "interval={interval}".format(name = name, host = host,
                    port = port, xprt = xprt, type = type, 
                    interval = reconnect_interval)

    @classmethod
    def prdcr_del(cls, name):
        return "prdcr_del name={}".format(name)

    @classmethod
    def prdcr_start(cls, name):
        return "prdcr_start name={)".format(name)

    @classmethod
    def prdcr_stop(cls, name):
        return "prdcr_stop name={}".format(name)

    @classmethod
    def updtr_add(cls, name, update_interval, update_offset,
                  push = None, perm = None, prdcrs = [], 
                  set_matches = {'set_name': [], 'schema': []}):
        cmd = "updtr_add name={name} interval={interval} offset={offset}".format(
                    name = name, interval = update_interval, offset = update_offset)
        if push is not None:
            cmd += " push={}".format(push)
        if perm is not None:
            cmd += " perm={}".format(perm)

        cmd += cls.updtr_prdcr_add(name, prdcrs)

        cmd += cls.updtr_match_add(name, set_matches)

        return cmd

    @classmethod
    def updtr_prdcr_add(cls, name, prdcrs):
        cnt = 0
        cmd = ""
        for reg in prdcrs_regexs:
            if cnt > 0:
                cmd += "\n"
            cmd += "updtr_prdcr_add name=%s regex=%s" % (name, reg)
            cnt += 1
        return cmd

    @classmethod
    def updtr_prdcr_del(cls, name, prdcrs):
        cnt = 0
        cmd = ""
        for reg in prdcrss:
            if cnt > 0:
                cmd += "\n"
            cmd += "updtr_prdcr_del name=%s regex=%s" % (name, reg)
            cnt += 1
        return cmd

    @classmethod
    def updtr_match_add(cls, name, set_matches):
        cnt = 0
        cmd = ""
        if len(set_matches['set_name']) > 0:
            for reg in set_matches['set_name']:
                if cnt > 0:
                    cmd += "\n"
                cmd += "updtr_match_add name=%s regex=%s match=inst" % (name, reg)
                cnt += 1

        if len(set_matches['schema']) > 0:
            for reg in set_matches['schema']:
                if cnt > 0:
                    cmd += "\n"
                cmd += "updtr_match_add name=%s regex=%s match=schema" % (name, reg)
                cnt += 1

        return cmd

    @classmethod
    def updtr_match_del(cls, name, set_match_regexs):
        cnt = 0
        cmd = ""
        if len(set_match_regexs['set_name']) > 0:
            for reg in set_match_regexs['set_name']:
                if cnt > 0:
                    cmd += "\n"
                cmd += "updtr_match_del name=%s regex=%s match=inst" % (name, reg)
                cnt += 1

        if len(set_match_regexs['schema']) > 0:
            for reg in set_match_regexs['schema']:
                if cnt > 0:
                    cmd += "\n"
                cmd += "updtr_match_del name=%s regex=%s match=schema" % (name, reg)
                cnt += 1

        return cmd

    @classmethod
    def updtr_del(cls, name):
        return "updtr_del name=%s" % (name)

    @classmethod
    def updtr_start(cls, name, update_interval = None, update_offset = None):
        cmd = "updtr_start name=%s" % (name)
        if update_interval is not None:
            cmd += " interval=%s" % (update_interval)
        if update_offset is not None:
            cmd += " offset=%s" % (update_offset)
        return cmd

    @classmethod
    def updtr_stop(cls, name):
        return "updtr_stop name=%s" % (name)

    @classmethod
    def strgp_add(cls, name, container, schema, plugin, perm = None,
                  prdcrs = [], metrics = []):
        cmd = "strgp_add name={name} container={container} schema={schema} " \
                "plugin={plugin}".format(name = name, container = container,
                                         schema = schema, plugin = plugin)
        if perm is not None:
            cmd += " perm=%s" % (perm)

        cmd += cls.strgp_prdcr_add(name, prdcrs)
        cmd += cls.strgp_metric_add(name, metrics)
        

    @classmethod
    def strgp_prdcr_add(cls, name, prdcrs):
        cnt = 0
        cmd = ""
        for p in prdcrs:
            if cnt > 0:
                cmd += "\n"
            cmd += "strgp_prdcr_add name=%s regex=%s" % (name, p)
            cnt += 1
        return cmd

    @classmethod
    def strgp_metric_add(cls, name, metrics):
        cnt = 0
        cmd = ""
        for m in metrics:
            if cnt > 0:
                cmd += "\n"
            cmd += "strgp_metric_add name=%s metric=%s" % (name, m)
            cnt += 1
        return cmd

    @classmethod
    def strgp_del(cls, name):
        return "strgp_del name=%s" % (name)

    @classmethod
    def strgp_start(cls, name):
        return "strgp_start name=%s" % (name)

    @classmethod
    def strgp_stop(cls, name):
        return "strgp_stop name=%s" % (name)

class LDMSD_CFG_CMD_V5(LDMSD_CFG_CMD):

    @classmethod
    def prdcr_add(cls, name, host, port, xprt, type, reconnect_interval):
        pass