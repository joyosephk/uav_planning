; UAV Mission Planning - SINGLE UAV version
;
; -Utilizes conditional dynamics (ADL)
;
; Created by Joseph Kim


(define (domain uav)
(:requirements :fluents :adl)
(:predicates 
  (at ?y)
  (require_surveil ?y)
  (require_intercept ?y)
  (require_package ?y)
)

(:functions
  (distance ?y ?z)
  (fuel)
  (fuel_capacity)
  (packagecount)
  (package_capacity)
  (cost_surveil)
  (cost_intercept)
  (num_resolved)
  (totalFuelUsage)
)


(:action goto
:parameters (?y ?z) 
:precondition (and 
  (at ?y) 
  (>= (fuel) (distance ?y ?z))
)

:effect (and 
  (increase (totalFuelUsage) (distance ?y ?z))
  (not (at ?y)) 
  (at ?z)

  (when (= ?z base) 
        (assign (fuel) (fuel_capacity))
  )

  (when (not (= ?z base))
        (decrease (fuel) (distance ?y ?z))
  )

  (when (= ?z packagecenter) 
        (assign (packagecount) (package_capacity))
  )

)
)



(:action drop
:parameters (?w)
:precondition (and 
  (at ?w)
  (require_package ?w)
  (>= (packagecount) 1)
)

:effect (and 
  (decrease (fuel) 1)
  (decrease (packagecount) 1)
  (not (require_package ?w))
  (increase (num_resolved) 1)
  (increase (totalFuelUsage) 1)
)
)



(:action surveil
:parameters (?w)
:precondition (and 
  (at ?w)
  (require_surveil ?w)
  (>= (fuel) (cost_surveil))
)

:effect (and 
  (decrease (fuel) (cost_surveil))
  (not (require_surveil ?w))
  (increase (num_resolved) 1)
  (increase (totalFuelUsage) (cost_surveil))
)
)


(:action intercept
:parameters (?w)
:precondition (and 
  (at ?w)
  (require_intercept ?w)
  (>= (fuel) (cost_intercept))
)

:effect (and 
  (decrease (fuel) (cost_intercept))
  (not (require_intercept ?w))
  (increase (num_resolved) 1)
  (increase (totalFuelUsage) (cost_intercept))
)
)


)
