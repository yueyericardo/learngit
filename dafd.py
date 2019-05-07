import tensorflow as tf
import os

def load_sae(filename):
    """Returns tf tensor of self energy"""
    # self_energies = []
    # with open(filename) as f:
    #     for i in f:
    #         line = [x.strip() for x in i.split('=')]
    #         index = int(line[0].split(',')[1].strip())
    #         value = float(line[1])
    #         self_energies.append((index, value))
    # self_energies = [i for _, i in sorted(self_energies)]
    # self_energies_tf = tf.convert_to_tensor(self_energies)
    self_energies_tf = tf.convert_to_tensor([ -0.600953, -38.08316,  -54.707756, -75.194466])
    return self_energies_tf

class ANIModel:
    """ANI model that compute properties from species and AEVs.
    Different atom types might have different modules, when computing
    properties, for each atom, the module for its corresponding atom type will
    be applied to its AEV, after that, outputs of modules will be reduced along
    different atoms to obtain molecular properties.
    Arguments:
        modules (:class:`collections.abc.Sequence`): Modules for each atom
            types. Atom types are distinguished by their order in
            :attr:`modules`, which means, for example ``modules[i]`` must be
            the module for atom type ``i``. Different atom types can share a
            module by putting the same reference in :attr:`modules`.
        reducer (:class:`collections.abc.Callable`): The callable that reduce
            atomic outputs into molecular outputs. It must have signature
            ``(tensor, dim)->tensor``.
        padding_fill (float): The value to fill output of padding atoms.
            Padding values will participate in reducing, so this value should
            be appropriately chosen so that it has no effect on the result. For
            example, if the reducer is :func:`torch.sum`, then
            :attr:`padding_fill` should be 0, and if the reducer is
            :func:`torch.min`, then :attr:`padding_fill` should be
            :obj:`math.inf`.
    """
    def __init__(self, modules, self_energies_tf):
        self.modules = modules
        # path = os.path.dirname(__file__)
        # sae_file = os.path.join(path, 'resources/ani-1x_dft_x8ens/sae_linfit.dat')
        # self.self_energies = load_sae(sae_file)
        self.self_energies = tf.convert_to_tensor(self_energies_tf)
    # @tf.contrib.eager.defun
    # @tf.contrib.autograph.convert()
    def __call__(self, species_aev):
    # def __call__(self):

        # species = tf.placeholder(dtype=tf.float32, shape=[None, None])
        # aev = tf.placeholder(dtype=tf.float32, shape=[None, None, 384])

        # return(tf.add(species, aev))
        species, aev = species_aev

        species_ = tf.reshape(species, [-1])

        # print("species: ",species_)
        # present_species = AEV.present_species(species)
        # print("present_species: ", present_species.size())
        # print("aev: ", aev)

        resize_list = tf.reduce_prod(tf.shape(aev)[:2]), tf.shape(aev)[2]

        aev = tf.reshape(aev, resize_list)
        # print("aev: ", aev)

        output = tf.zeros_like(species_, dtype=aev.dtype)
        e_each_species = []
        mask_each_species = []
        for i in range(4):
            mask = tf.math.equal(species_, i)
            mask_number = tf.expand_dims(tf.cast(mask, dtype=tf.float32), 1)
            aev_mask = tf.multiply(mask_number, aev)
            input_ = aev_mask

            # aev to energy
            e_this_specie = self.modules[i](input_)
            e_each_species.append(e_this_specie)
            mask_each_species.append(mask)
            print("e_this_specie: ", e_this_specie.shape)
            e_this_specie = tf.reduce_sum(e_this_specie, -1, keepdims=True)
            print("e_this_specie: ", e_this_specie.shape)
            
            # add energy shift
            e_this_specie_shift = tf.add(e_this_specie, self.self_energies[i])

            # reset the energy of other species
            output_mask = tf.squeeze(tf.multiply(mask_number, e_this_specie_shift))
            output = tf.add(output, output_mask)

        for i in range(len(e_each_species)):
            # reshape mask to [Molecules, Atoms, 1]
            mask_each_species[i] = tf.reshape(mask_each_species[i], [tf.shape(species)[0], tf.shape(species)[1], 1])

            # add energy shift
            e_each_species[i] = tf.add(e_each_species[i], self.self_energies[i])
#             print(tf.shape(e_each_species[i]))
#             print(self.self_energies[i])
            
            if (i == 0):
                # add energy shift
                print(e_each_species[i])
                print('-'*30)
                e_each_species[i] = tf.add(e_each_species[i], self.self_energies[i]/2)
                print(e_each_species[i])
                # reshape energy to [Molecules, Atoms, 2]
                e_each_species[i] = tf.reshape(e_each_species[i], [tf.shape(species)[0], tf.shape(species)[1], 2])
                # reset the energy of other species
                mask_each_species[i] = tf.broadcast_to(mask_each_species[i], tf.shape(e_each_species[i]))
                e_each_species[i] = tf.where(mask_each_species[i], e_each_species[i], tf.zeros_like(e_each_species[i]))
                # print(e_each_species[i].shape)
                e_each_species[i] = tf.pad(e_each_species[i], paddings=[[0, 0], [0, 0], [0, 15 - 2]])
            else:
                # add energy shift
                print(e_each_species[i])
                print('-'*30)
                e_each_species[i] = tf.add(e_each_species[i], self.self_energies[i]/15)
                print(e_each_species[i])
                # reshape energy to [Molecules, Atoms, 15]
                e_each_species[i] = tf.reshape(e_each_species[i], [tf.shape(species)[0], tf.shape(species)[1], 15])
                # reset the energy of other species
                mask_each_species[i] = tf.broadcast_to(mask_each_species[i], tf.shape(e_each_species[i]))
                e_each_species[i] = tf.where(mask_each_species[i], e_each_species[i], tf.zeros_like(e_each_species[i]))
                
#             print(e_each_species[i].shape)
#             print(e_each_species[i])
            
        def pad_AO(AO_all):
            boolean_mask = tf.logical_not(tf.equal(AO_all, tf.zeros_like(AO_all)))

            # all the non-zero values in a flat tensor
            non_zero_values = tf.gather_nd(AO_all, tf.where(boolean_mask))
            # number of non-zero values in each row
            n_non_zero = tf.count_nonzero(AO_all, -1)  
#             n_non_zero = tf.reduce_sum(tf.cast(boolean_mask, tf.int64), axis=-1)
            # max number of non-zeros -> this will be the padding length
            max_non_zero = tf.reduce_max(n_non_zero).numpy() 
            
            # Split the tensor into flat tensors with the non-zero values of each row
            rows = tf.split(non_zero_values, n_non_zero)

            # Pad with zeros wherever necessary and recombine into a single tensor
            return tf.stack([tf.pad(r, paddings=[[0, max_non_zero - r.get_shape().as_list()[0]]]) for r in rows])
        
        # TODO try to use accumulate_n to save memory
        # https://www.tensorflow.org/api_docs/python/tf/math/accumulate_n
        e_each_species_sum = tf.math.add_n(e_each_species)
#         print(e_each_species_sum)
        e_each_species_sum = tf.reshape(e_each_species_sum, [tf.shape(species)[0], -1] )
#         print(e_each_species_sum)
        e_each_species_sum = pad_AO(e_each_species_sum)
        print(e_each_species_sum)
        print(species)
        output = tf.reshape(output, tf.shape(species))
        return species, tf.math.reduce_sum(output, axis=1)
