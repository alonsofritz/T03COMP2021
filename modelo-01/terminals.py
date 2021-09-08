""" Dicionários usados para facilitar a identificação de tokens da linguagem. """

# Delimitadores => t1
delimiters = dict({
    't100' : 'DEL_LP',    # (
    't101' : 'DEL_RP',    # )
    't102' : 'DEL_LCB',   # {
    't103' : 'DEL_RCB',   # }
    't104' : 'DEL_QUO',   # ',
    't105' : 'DEL_COM',   # ,
    't106' : 'DEL_SC',    # ;
})

# Palavras reservadas = t2
keywords = dict({
    't200' : 'KW_an',
    't201' : 'KW_car',
    't202' : 'KW_cela',
    't203' : 'KW_entulesse',
    't204' : 'KW_ista',
    't205' : 'KW_qui',
    't206' : 'KW_sarme',
    't207' : 'KW_celace',
    't208' : 'KW_hyaline',
    't209' : 'KW_note',
    't210' : 'KW_liltengwa',
    't211' : 'KW_yulmavene',
    't212' : 'KW_true',
    't213' : 'KW_false',
    't214' : 'KW_hyaline',
})

# Constantes = t3
constants = dict({
    't300' : 'id',
    't301' : 'number',
    't302' : 'string',
    't303' : 'boolean',
})

# Operadores = t4
operators = dict({
    't400' : 'OP_ADD',       # +
    't401' : 'OP_MIN',       # -
    't402' : 'OP_MUL',       # *
    't403' : 'OP_DIV',       # /
    't404' : 'OP_MOD',       # %
    't405' : 'OP_PP',        # ++
    't406' : 'OP_MM',        # --
    't407' : 'OP_EQ',        # ==
    't408' : 'OP_NE',        # !=
    't409' : 'OP_ASS',       # =
    't410' : 'OP_GT',        # >
    't411' : 'OP_GE',        # >=
    't412' : 'OP_LT',        # <
    't413' : 'OP_LE',        # <=
    't414' : 'OP_ar',        # and
    't415' : 'OP_hela',      # or
    't416' : 'OP_la',        # not
    't417' : 'OP_helaer',    # xor
})

"""
types = dict({
    'del' : delimiters,
    'kw' : keywords,
    'cons' : constants,
    'op' : operators
})
"""