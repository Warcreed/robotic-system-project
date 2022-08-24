from lib.data.plot import *

class Telemetry:

    def __init__(self):
        self.plotter = DataPlotter()         

    def gather(self, delta_t,  base_joint, second_joint, end_effector_joint):
        self.plotter.add('t', delta_t)

        # base_joint
        self.plotter.add('base_theta_ref', base_joint[0])    # theta from inverse_kinematics
        self.plotter.add('base_theta', base_joint[1])        # theta from self.arm.element_N.theta
        self.plotter.add('base_w_target', base_joint[2])     # w target from self.arm.element_N_control.w_target
        self.plotter.add('base_w', base_joint[3])            # w from position control
        self.plotter.add('base_torque', base_joint[4])       # torque from speed control

        # second_joint
        self.plotter.add('second_theta_ref', second_joint[0])    # theta from inverse_kinematics
        self.plotter.add('second_theta', second_joint[1])        # theta from self.arm.element_N.theta
        self.plotter.add('second_w_target', second_joint[2])     # w target from self.arm.element_N_control.w_target
        self.plotter.add('second_w', second_joint[3])            # w from position control
        self.plotter.add('second_torque', second_joint[4])       # torque from speed control

        # end effector
        self.plotter.add('end_eff_theta_ref', end_effector_joint[0])    # theta from inverse_kinematics
        self.plotter.add('end_eff_theta', end_effector_joint[1])        # theta from self.arm.element_N.theta
        self.plotter.add('end_eff_w_target', end_effector_joint[2])     # w target from self.arm.element_N_control.w_target
        self.plotter.add('end_eff_w', end_effector_joint[3])            # w from position control
        self.plotter.add('end_eff_torque', end_effector_joint[4])       # torque from speed control

    def show(self, print_base_joint= False, print_second_joint= False, print_end_eff_joint= False):
        # base_joint
        if print_base_joint:
            self.plotter.plot( [ 't', 'Time' ],
                                [ [ 'base_theta_ref', 'Base Theta Ref'] , [ 'base_theta', 'Base Theta' ] ])
            self.plotter.plot( [ 't', 'Time' ],
                                [ [ 'base_w_target', 'Base W Target'], [ 'base_w', 'Base W']  ])
            self.plotter.plot( [ 't', 'Time' ],
                                [ [ 'base_torque', 'Base Torque']  ])

        # second_joint
        if print_second_joint:
            self.plotter.plot( [ 't', 'Time' ],
                                [ [ 'second_theta_ref', 'Second Theta Ref'] , [ 'second_theta', 'Second Theta' ] ])
            self.plotter.plot( [ 't', 'Time' ],
                                [ [ 'second_w_target', 'Second W Target'], [ 'second_w', 'Second W']  ])
            self.plotter.plot( [ 't', 'Time' ],
                                [ [ 'second_torque', 'Second Torque']  ])

        # end effector
        if print_end_eff_joint:
            self.plotter.plot( [ 't', 'Time' ],
                                [ [ 'end_eff_theta_ref', 'End Eff Theta Ref'] , [ 'end_eff_theta', 'End Eff Theta' ] ])
            self.plotter.plot( [ 't', 'Time' ],
                                [ [ 'end_eff_w_target', 'End Eff W Target'], [ 'end_eff_w', 'End Eff W']  ])
            self.plotter.plot( [ 't', 'Time' ],
                                [ [ 'end_eff_torque', 'End Eff Torque']  ])

        self.plotter.show()




