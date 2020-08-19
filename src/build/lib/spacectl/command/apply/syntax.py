def create_spaceone_apply_manitest(yaml_list):
    # yaml을 읽은 후 생성된 list를 이용해 SpaceoneApplyManifest 생성
    # var, env 오버라이딩 및 설정
    pass


def get_key(key, value, context=None):
    # key가 $로 시작하는 spaceone의 부가적인 logic을 수행해야하는 구문인지 단순 key인지
    # 아직 로직에 대한 생각은 없음.
    if _is_spaceone_logic(key):
        return _exec_spaceone_logic(key, value, context)
    else:
        return key


def get_value(value, context=None):
    is_raw_value = True
    # raw_value인지 context를 이용하는 지 판별 e.g. "grpc://identity:50051" or ${{ spaceone.identity.endpoint }}
    if is_raw_value:
        return value
    else:
        # context를 통해 value를 연산
        return _get_value_from_context(value)


def get_condition(condition, raw=True):
    if raw:
        return _exec_condition(condition)


def _is_spaceone_logic(key):
    pass


def _exec_spaceone_logic(key, value):
    pass


def _get_value_from_context(value):
    # _get_value_from_context
    pass


def _exec_condition(condition):
    pass